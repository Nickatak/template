import globals from "globals";
import js from "@eslint/js";
import ts from "typescript-eslint";

export default [
  {
    ignores: ["node_modules/", ".next/", "out/", "dist/", "build/"],
  },
  js.configs.recommended,
  ...ts.configs.recommended,
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    languageOptions: {
      globals: {
        ...globals.browser,
      },
      parser: ts.parser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    rules: {
      "react/react-in-jsx-scope": "off",
    },
  },
];
