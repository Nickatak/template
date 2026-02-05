# Authentication End-to-End Tests

This document describes the comprehensive test suite for all authentication functions in the application.

## Overview

The test suite includes two types of tests:

1. **API Tests** (`test_auth_api.py`) - Direct HTTP tests of authentication endpoints
2. **E2E Tests** (`test_auth_e2e.py`) - Browser-based tests simulating real user interactions

## Setup

### 1. Install Test Dependencies

```bash
make install
```

This installs all required testing packages from `requirements.txt`:
- `pytest` - Test framework
- `pytest-django` - Django integration
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for API tests
- `playwright` - Browser automation for E2E tests

### 2. Initialize Playwright Browsers

For E2E tests, you need to install Playwright browsers:

```bash
.venv/bin/playwright install
```

## Running Tests

### All Tests

```bash
make test
```

Runs both API and E2E tests with verbose output.

### API Tests Only

```bash
make test-api
```

Tests all authentication endpoints directly without browser automation:
- Registration endpoint
- Login endpoint
- Profile endpoint
- User search endpoint
- Token handling

### E2E Tests Only

```bash
make test-e2e
```

Tests complete authentication flows through the browser UI.

**Note:** E2E tests require both Django and Next.js servers running:

```bash
# In one terminal
make run-backend

# In another terminal
make run-frontend

# In a third terminal
make test-e2e
```

### Authentication Tests Only

```bash
make test-auth
```

Runs only tests marked with the `@pytest.mark.auth` decorator.

### Tests with Coverage

```bash
make test-cov
```

Runs tests and generates a coverage report in `htmlcov/index.html`.

### Watch Mode

```bash
make test-watch
```

Automatically reruns tests when files change.

## Test Coverage

### Registration Tests

Tests the `POST /api/auth/register/` endpoint:
- ✅ Successful registration with valid credentials
- ✅ Duplicate email prevention
- ✅ Password mismatch validation
- ✅ Password length validation
- ✅ Invalid email format
- ✅ Missing required fields
- ✅ UI registration flow
- ✅ Error message display

### Login Tests

Tests the `POST /api/auth/login/` endpoint:
- ✅ Successful login with valid credentials
- ✅ Invalid email handling (returns generic error)
- ✅ Invalid password handling (returns generic error)
- ✅ Empty email validation
- ✅ Empty password validation
- ✅ Missing required fields
- ✅ Token response validation
- ✅ UI login flow with redirect to dashboard
- ✅ Failed login email retention

### Profile Tests

Tests the `GET/PUT /api/auth/profile/` endpoints:
- ✅ Retrieve profile when authenticated
- ✅ Retrieve profile fails without authentication
- ✅ Update email successfully
- ✅ Duplicate email prevention
- ✅ Same email update (no-op)
- ✅ Update fails without authentication
- ✅ Profile view through UI
- ✅ Profile update through UI

### Token Tests

Tests JWT token handling:
- ✅ Token payload contains user ID
- ✅ Invalid token rejection
- ✅ Malformed authorization header handling
- ✅ Token persistence across navigation
- ✅ Token storage in browser

### User Search Tests

Tests the `GET /api/auth/search-users/` endpoint:
- ✅ Search users when authenticated
- ✅ Minimum search length (2 characters)
- ✅ Case-insensitive search
- ✅ Result limiting (max 10)

### Integration Tests

Complete authentication flows:
- ✅ Register → Login → Access Profile
- ✅ Login → Update Profile
- ✅ Navigation between login and register
- ✅ Logout flow
- ✅ Session persistence

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_auth_api.py         # API-level tests
├── test_auth_e2e.py         # Browser-based E2E tests
└── pytest.ini              # Pytest settings
```

## Fixtures

### Database Fixtures

```python
db_reset                      # Clean database before each test
test_user                     # Pre-created test user
test_user_data               # Valid registration data
invalid_user_data            # Invalid registration data
```

### HTTP Client Fixtures

```python
http_client                   # Sync HTTP client
async_http_client            # Async HTTP client
authenticated_client         # HTTP client with JWT token
login_response              # Login response with tokens
```

### Browser Fixtures

```python
browser                       # Playwright browser instance
browser_context             # Browser context for E2E tests
page                        # Browser page for navigation
```

### Assertion Fixtures

```python
assert_user_created()       # Assert user was created
assert_user_not_created()   # Assert user was not created
```

## Configuration

### pytest.ini

Controls test discovery and behavior:
- Sets Django settings module
- Defines custom markers
- Configures test output

### conftest.py

Sets up:
- Django ORM access
- HTTP clients
- Browser automation
- Test fixtures
- Database cleanup

## Authentication Test Markers

Tests are marked with decorators for easy filtering:

```python
@pytest.mark.auth           # All authentication tests
@pytest.mark.registration  # Registration tests
@pytest.mark.login         # Login tests
@pytest.mark.profile       # Profile tests
@pytest.mark.e2e          # Browser-based E2E tests
@pytest.mark.integration  # Integration tests
```

Run tests by marker:

```bash
pytest -m auth              # All auth tests
pytest -m registration      # Registration only
pytest -m "auth and login"  # Auth login tests
pytest -m "not e2e"         # All tests except E2E
```

## Environment Variables

Configure test behavior with environment variables:

```bash
# API server location (default: http://localhost:8000)
export DJANGO_TEST_HOST=http://localhost:8000

# Frontend location (default: http://localhost:3000)
export FRONTEND_TEST_HOST=http://localhost:3000
```

## Troubleshooting

### E2E Tests Timeout
- Ensure both Django and Next.js servers are running
- Check servers are accessible at the configured URLs
- Increase timeout values for slower machines

### Database Lock Errors
- Ensure no other Django processes are running
- Clear temporary databases: `rm db.sqlite3`
- Run `make test` with clean database

### Playwright Browser Issues
- Reinstall browsers: `.venv/bin/playwright install`
- Run with `--headed` to see browser window:
  ```bash
  pytest tests/test_auth_e2e.py --headed
  ```

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `make install`
- Check `PYTHONPATH` includes project root

## CI/CD Integration

For continuous integration, use:

```bash
# Run tests without X display (headless)
pytest tests/test_auth_api.py  # API tests don't need browser

# Run E2E tests with xvfb-run (Linux)
xvfb-run pytest tests/test_auth_e2e.py

# Generate coverage report
make test-cov
```

## Best Practices

1. **Keep tests focused** - Each test should verify one behavior
2. **Use fixtures** - Avoid duplicating setup code
3. **Test both success and failure** - Cover happy path and errors
4. **Use meaningful names** - Test names should describe what's tested
5. **Clean up** - Tests should not depend on each other
6. **Mock external services** - Isolate the code being tested

## Adding New Tests

### For New API Endpoints

1. Add test class to `test_auth_api.py`
2. Use `http_client` fixture for requests
3. Mark with appropriate decorators
4. Follow existing test patterns

Example:

```python
@pytest.mark.auth
class TestNewEndpoint:
    def test_successful_operation(self, http_client):
        response = http_client.post("/api/auth/new/", json={...})
        assert response.status_code == 200
```

### For New UI Flows

1. Add test class to `test_auth_e2e.py`
2. Use `page` fixture for navigation
3. Use async/await for asynchronous operations
4. Mark with `@pytest.mark.e2e`

Example:

```python
@pytest.mark.e2e
class TestNewFlow:
    @pytest.mark.asyncio
    async def test_user_flow(self, page):
        await page.goto("http://localhost:3000/new-page")
        # ... test assertions
```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Playwright Python](https://playwright.dev/python/)
- [httpx Documentation](https://www.python-httpx.org/)
