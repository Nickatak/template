from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for authentication operations.
    """

    def get_permissions(self):
        """
        Assign permissions based on the action.
        - register: AllowAny
        - login: AllowAny
        - profile: IsAuthenticated
        """
        if self.action in ["register", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["post"])
    def login(self, request):
        """Authenticate credentials and return JWT token pair.

        Contract:
        - `POST`:
          - `200`: credentials accepted and token pair returned.
            - Guarantees:
              - response includes both `access` and `refresh` tokens. `[APP]`
          - `400`: payload missing required fields.
            - Guarantees: no object mutations. `[APP]`
          - `401`: credentials rejected.
            - Guarantees: no object mutations. `[APP]`

        - Preconditions:
          - none (`AllowAny`).

        - Object mutations:
          - `POST`:
            - Creates:
              - Standard: none.
              - Audit: none.
            - Edits:
              - Standard: none.
              - Audit: none.
            - Deletes: none.

        - Incoming payload (`POST`) shape:
          - JSON map:
            {
              "email": "string (required)",
              "password": "string (required)"
            }

        - Idempotency and retry semantics:
          - `POST` is retry-safe for invalid credentials (read-only failure path).
          - `POST` is not idempotent in token value issuance semantics.

        - Test anchors:
          - `backend/tests/test_auth_api.py::TestLogin::test_successful_login`
          - `backend/tests/test_auth_api.py::TestLogin::test_login_invalid_email`
          - `backend/tests/test_auth_api.py::TestLogin::test_login_invalid_password`
          - `backend/tests/test_auth_api.py::TestLogin::test_login_empty_email`
          - `backend/tests/test_auth_api.py::TestLogin::test_login_empty_password`
        """
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "")

        if not email:
            return Response(
                {"email": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"password": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if user exists
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "Email or password is incorrect."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Try to get token using the serializer
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        # If serializer fails, provide generic error message for security
        return Response(
            {"detail": "Email or password is incorrect."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(detail=False, methods=["post"])
    def register(self, request):
        """Register a new user account.

        Contract:
        - `POST`:
          - `201`: user created and serialized profile returned.
            - Guarantees:
              - a new user row exists for the submitted unique email. `[DB+APP]`
              - response excludes raw password fields. `[APP]`
          - `400`: payload invalid or email already exists.
            - Guarantees: no durable partial mutation from failed request path. `[DB+APP]`

        - Preconditions:
          - none (`AllowAny`).

        - Object mutations:
          - `POST`:
            - Creates:
              - Standard: user account.
              - Audit: none.
            - Edits:
              - Standard: none.
              - Audit: none.
            - Deletes: none.

        - Incoming payload (`POST`) shape:
          - JSON map:
            {
              "email": "string (required, unique)",
              "password": "string (required)",
              "password_confirm": "string (required; matches password)"
            }

        - Idempotency and retry semantics:
          - `POST` is not idempotent for new unique identities.
          - retrying successful payload with the same email returns validation error.

        - Test anchors:
          - `backend/tests/test_auth_api.py::TestRegistration::test_successful_registration`
          - `backend/tests/test_auth_api.py::TestRegistration::test_registration_duplicate_email`
          - `backend/tests/test_auth_api.py::TestRegistration::test_registration_password_mismatch`
          - `backend/tests/test_auth_api.py::TestRegistration::test_registration_missing_fields`
        """
        if User.objects.filter(email=request.data.get("email")).exists():
            return Response(
                {"email": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get", "put"])
    def profile(self, request):
        """Read or update the authenticated user's profile.

        Contract:
        - `GET`:
          - `200`: current user profile returned.
            - Guarantees: profile reflects persisted user state. `[APP]`
          - `401`: authentication missing/invalid.
            - Guarantees: no object mutations. `[APP]`
        - `PUT`:
          - `200`: profile updated and returned.
            - Guarantees:
              - updated email remains unique across users. `[DB+APP]`
              - persisted user profile matches the response body. `[APP]`
          - `400`: payload invalid (including duplicate email conflict).
            - Guarantees: no durable partial mutation from failed request path. `[DB+APP]`
          - `401`: authentication missing/invalid.
            - Guarantees: no object mutations. `[APP]`

        - Preconditions:
          - caller must be authenticated (`IsAuthenticated`).

        - Object mutations:
          - `GET`: none.
          - `PUT`:
            - Creates:
              - Standard: none.
              - Audit: none.
            - Edits:
              - Standard: authenticated `User` row (email only when provided and valid).
              - Audit: none.
            - Deletes: none.

        - Incoming payload (`PUT`) shape:
          - JSON map:
            {
              "email": "string (optional; must be unique if provided)"
            }

        - Idempotency and retry semantics:
          - `GET` is idempotent and read-only.
          - `PUT` is conditionally idempotent when retried with unchanged values.

        - Test anchors:
          - `backend/tests/test_auth_api.py::TestProfile::test_get_profile_authenticated`
          - `backend/tests/test_auth_api.py::TestProfile::test_get_profile_unauthenticated`
          - `backend/tests/test_auth_api.py::TestProfile::test_update_profile_email`
          - `backend/tests/test_auth_api.py::TestProfile::test_update_profile_duplicate_email`
          - `backend/tests/test_auth_api.py::TestProfile::test_update_profile_unauthenticated`
        """
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        elif request.method == "PUT":
            user = request.user

            if "email" in request.data:
                if (
                    User.objects.filter(email=request.data["email"])
                    .exclude(id=user.id)
                    .exists()
                ):
                    return Response(
                        {"email": "Email already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.email = request.data["email"]

            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search_users(self, request):
        """Search users by email substring with small result window.

        Contract:
        - `GET`:
          - `200`: filtered user list returned (possibly empty).
            - Guarantees:
              - response contains at most 10 `(id, email)` entries. `[APP]`
              - query length `< 2` returns `[]` without DB mutation. `[APP]`
          - `401`: authentication missing/invalid.
            - Guarantees: no object mutations. `[APP]`

        - Preconditions:
          - caller must be authenticated (`IsAuthenticated`).

        - Object mutations:
          - `GET`: none.

        - Idempotency and retry semantics:
          - `GET` is idempotent and read-only.

        - Test anchors:
          - `backend/tests/test_auth_api.py::TestUserSearch::test_search_users_authenticated`
          - `backend/tests/test_auth_api.py::TestUserSearch::test_search_users_minimum_length`
          - `backend/tests/test_auth_api.py::TestUserSearch::test_search_users_limit`
        """
        query = request.query_params.get("q", "").strip()

        if len(query) < 2:
            return Response([], status=status.HTTP_200_OK)

        users = User.objects.filter(Q(email__icontains=query)).values("id", "email")[
            :10
        ]  # Limit to 10 results

        return Response(list(users), status=status.HTTP_200_OK)
