#!/usr/bin/env python3
"""Enforce REST route contract docstring structure for backend API views."""

from __future__ import annotations

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VIEWS_DIR = ROOT / "backend" / "api" / "views"

REQUIRED_SECTION_TITLES = (
    "Contract:",
    "- Preconditions:",
    "- Object mutations:",
    "- Idempotency and retry semantics:",
    "- Test anchors:",
)
WRITE_METHODS = {"POST", "PUT", "PATCH"}
GUARANTEE_TAG_RE = re.compile(r"\[(DB\+APP|DB|APP)\]")


@dataclass(frozen=True)
class RouteDocTarget:
    file_path: Path
    function_name: str
    line_number: int
    methods: tuple[str, ...]
    docstring: str | None

    @property
    def location(self) -> str:
        return f"{self.file_path}:{self.line_number}"


def _decorator_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _extract_str_literals(node: ast.AST | None) -> list[str]:
    if node is None:
        return []
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        values: list[str] = []
        for item in node.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                values.append(item.value)
        return values
    return []


def _extract_methods_from_decorator(decorator: ast.AST) -> set[str]:
    methods: set[str] = set()
    if not isinstance(decorator, ast.Call):
        return methods

    name = _decorator_name(decorator.func)
    if name == "api_view":
        source = decorator.args[0] if decorator.args else None
        methods.update(s.upper() for s in _extract_str_literals(source))
    elif name == "action":
        source = None
        for keyword in decorator.keywords:
            if keyword.arg == "methods":
                source = keyword.value
                break
        # DRF defaults @action methods to GET when omitted.
        if source is None:
            methods.add("GET")
        else:
            methods.update(s.upper() for s in _extract_str_literals(source))

    return methods


def _iter_route_targets(module: ast.Module, file_path: Path) -> Iterable[RouteDocTarget]:
    viewset_method_map = {
        "list": "GET",
        "retrieve": "GET",
        "create": "POST",
        "update": "PUT",
        "partial_update": "PATCH",
        "destroy": "DELETE",
    }
    http_methods = {"get", "post", "put", "patch", "delete", "head", "options"}

    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods: set[str] = set()
            for decorator in node.decorator_list:
                methods |= _extract_methods_from_decorator(decorator)
            if not methods:
                continue
            yield RouteDocTarget(
                file_path=file_path,
                function_name=node.name,
                line_number=node.lineno,
                methods=tuple(sorted(methods)),
                docstring=ast.get_docstring(node),
            )
            continue

        if not isinstance(node, ast.ClassDef):
            continue

        base_names = {_decorator_name(base) for base in node.bases}
        is_viewset = any(name and name.endswith("ViewSet") for name in base_names)
        is_apiview = any(name and name.endswith("APIView") for name in base_names)

        for member in node.body:
            if not isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            methods: set[str] = set()
            for decorator in member.decorator_list:
                methods |= _extract_methods_from_decorator(decorator)

            if not methods and is_apiview and member.name in http_methods:
                methods.add(member.name.upper())
            if not methods and is_viewset and member.name in viewset_method_map:
                methods.add(viewset_method_map[member.name])
            if not methods:
                continue

            yield RouteDocTarget(
                file_path=file_path,
                function_name=f"{node.name}.{member.name}",
                line_number=member.lineno,
                methods=tuple(sorted(methods)),
                docstring=ast.get_docstring(member),
            )


def _line_has_tag(line: str) -> bool:
    return GUARANTEE_TAG_RE.search(line) is not None


def _validate_docstring(target: RouteDocTarget) -> list[str]:
    errors: list[str] = []
    if target.docstring is None:
        return [f"{target.location} `{target.function_name}` missing docstring."]

    doc = target.docstring
    lines = [line.rstrip() for line in doc.splitlines()]

    for title in REQUIRED_SECTION_TITLES:
        if title not in doc:
            errors.append(
                f"{target.location} `{target.function_name}` missing section `{title}`."
            )

    for method in target.methods:
        token = f"- `{method}`:"
        if token not in doc:
            errors.append(
                f"{target.location} `{target.function_name}` missing contract entry `{token}`."
            )

    if set(target.methods) & WRITE_METHODS and "- Incoming payload" not in doc:
        errors.append(
            f"{target.location} `{target.function_name}` missing `Incoming payload` section for write method(s)."
        )

    if "Guarantees:" not in doc:
        errors.append(
            f"{target.location} `{target.function_name}` missing at least one `Guarantees` line."
        )
        return errors

    if GUARANTEE_TAG_RE.search(doc) is None:
        errors.append(
            f"{target.location} `{target.function_name}` missing guarantee source tag (`[DB]`, `[APP]`, `[DB+APP]`)."
        )

    in_multiline_guarantees = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if "Guarantees:" in stripped:
            if stripped.endswith("Guarantees:"):
                in_multiline_guarantees = True
            else:
                in_multiline_guarantees = False
                if not _line_has_tag(stripped):
                    errors.append(
                        f"{target.location} `{target.function_name}` guarantee line missing source tag: `{stripped}`."
                    )
            continue

        if not in_multiline_guarantees:
            continue

        if stripped.startswith("- `") or (
            stripped.startswith("- ")
            and stripped.endswith(":")
            and stripped[2:3].isupper()
        ):
            in_multiline_guarantees = False
            continue

        if stripped.startswith("- ") and not _line_has_tag(stripped):
            errors.append(
                f"{target.location} `{target.function_name}` guarantee bullet missing source tag: `{stripped}`."
            )

    return errors


def _iter_view_files(views_dir: Path) -> Iterable[Path]:
    for file_path in sorted(views_dir.rglob("*.py")):
        if file_path.name == "__init__.py":
            continue
        yield file_path


def run(views_dir: Path) -> int:
    if not views_dir.exists():
        print(f"error: views directory not found: {views_dir}", file=sys.stderr)
        return 2

    all_targets: list[RouteDocTarget] = []
    for file_path in _iter_view_files(views_dir):
        source = file_path.read_text(encoding="utf-8")
        module = ast.parse(source, filename=str(file_path))
        all_targets.extend(_iter_route_targets(module, file_path))

    if not all_targets:
        print(f"route-docstring-contract: no route handlers found under {views_dir}")
        return 0

    errors: list[str] = []
    for target in all_targets:
        errors.extend(_validate_docstring(target))

    if errors:
        print("route-docstring-contract: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"route-docstring-contract: ok ({len(all_targets)} route handlers checked)")
    return 0


if __name__ == "__main__":
    directory = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else DEFAULT_VIEWS_DIR.resolve()
    )
    raise SystemExit(run(directory))
