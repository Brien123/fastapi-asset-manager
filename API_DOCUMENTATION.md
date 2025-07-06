# Codexbase Network API Documentation

This document provides a detailed guide on how to use and test each endpoint of the Codexbase Network API.

### Testing without Local Setup

For convenience, you can test all API endpoints on a live, hosted version without setting up the project locally.
- **Interactive Docs (Swagger UI):** [https://fastapi-asset-manager.onrender.com/docs](https://fastapi-asset-manager.onrender.com/docs)
- **Base URL for API clients (cURL, Postman, etc.):** `https://fastapi-asset-manager.onrender.com`

When using the `cURL` examples in this document, simply replace the local base URL (`http://127.0.0.1:8000`) with the live one.

## 1. Getting Started: Authentication

All endpoints in this API (except for `/auth/`) are protected and require an **admin-level** JSON Web Token (JWT) for access.

### How to Authenticate

1.  **Use Default Admin Credentials**: The application automatically creates a default admin user on its first run. Use these credentials to get started:
    - **Username**: `admin`
    - **Password**: `12345678`

2.  **Get an Access Token**: Send a `POST` request to the `/auth/` endpoint with the default admin `username` and `password`. The API will return an `access_token`.
3.  **Use the Token**: For all subsequent requests to protected endpoints, include the token in the `Authorization` header.

**Example Header:**
`Authorization: Bearer <your_access_token>`

#### Authorizing in the Interactive Docs (Swagger UI)

To access protected endpoints that show a lock icon when using the interactive docs, you need to authorize your session:

1.  Click the **"Authorize"** button located at the top right of the page.
2.  In the popup, enter the default admin `username` and `password` into the form and click the "Authorize" button within the popup.
3.  Close the popup. The UI will now automatically include your authorization token in requests to protected routes.

## 2. API Endpoints

The following sections detail each available API endpoint.

---

### Authentication (`/auth`)

This endpoint is used to authenticate and receive a JWT.

#### **Get Access Token**

- **Purpose**: Authenticates a user with a username and password and returns an access token.
- **Endpoint**: `POST /auth/`
- **Authentication**: None
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Successful Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJI...",
    "token_type": "bearer"
  }
  ```
- **How to Test (cURL)**:
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/auth/' \
    -H 'Content-Type: application/json' \
    -d '{
      "username": "admin",
      "password": "12345678"
    }'
  ```

---

### Users (`/users`)

Endpoints for managing user accounts.

#### **Create a New User**

- **Purpose**: Registers a new user in the system. Can be an `admin` or a `user`.
- **Endpoint**: `POST /users/`
- **Authentication**: Required (Bearer Token, Admin Role)
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "a_strong_password"
  }
  ```
- **Successful Response (201 Created)**: Returns the newly created user object (without the password).
- **Error Responses**:
  - `400 Bad Request`: If the username or email is already registered.
- **How to Test (cURL)**:
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/users/' \
    -H 'Content-Type: application/json' \
    -d '{
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "a_strong_password"
    }'
  ```

#### **List All Users**

- **Purpose**: Retrieves a paginated list of all registered users.
- **Endpoint**: `GET /users/`
- **Authentication**: Required (Bearer Token)
- **Query Parameters**:
  - `page` (integer, default: 1): The page number to retrieve.
  - `limit` (integer, default: 20): The number of users per page.
- **Successful Response (200 OK)**: A paginated response object containing a list of users.
- **How to Test (cURL)**:
  ```bash
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  curl -X 'GET' \
    'http://127.0.0.1:8000/users/?page=1&limit=10' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
  ```

---

### Assets (`/assets`)

Endpoints for managing all financial assets on the platform. **Admin access is required.**

#### **Create a New Asset**

- **Purpose**: Creates a new financial asset (e.g., stock, crypto) and assigns it to a specific user.
- **Endpoint**: `POST /assets/`
- **Authentication**: Required (Bearer Token)
- **Request Body**:
  ```json
  {
    "name": "Apple Inc.",
    "type": "stock",
    "value": 1500.75,
    "owner_id": 1
  }
  ```
- **Successful Response (201 Created)**: Returns the newly created asset object.
- **How to Test (cURL)**:
  ```bash
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  curl -X 'POST' \
    'http://127.0.0.1:8000/assets/' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "Apple Inc.",
      "type": "stock",
      "value": 1500.75
    }'
  ```

#### **List User's Assets**

- **Purpose**: Retrieves a paginated list of all assets owned by the authenticated user.
- **Endpoint**: `GET /assets/`
- **Authentication**: Required (Bearer Token)
- **Query Parameters**:
  - `page` (integer, default: 1): The page number to retrieve.
  - `limit` (integer, default: 20): The number of assets per page.
- **Successful Response (200 OK)**: A paginated response object containing a list of the user's assets.
- **How to Test (cURL)**:
  ```bash
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  curl -X 'GET' \
    'http://127.0.0.1:8000/assets/?page=1&limit=5' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
  ```

---

### Transactions (`/transactions`)

Endpoint for logging financial transactions.

#### **Create a New Transaction**

- **Purpose**: Creates a new transaction for an asset owned by the authenticated user. This automatically updates the asset's value.
  - A `buy` transaction increases the asset's value.
  - A `sell` transaction decreases the asset's value.
- **Endpoint**: `POST /transactions/`
- **Authentication**: Required (Bearer Token)
- **Request Body**:
  ```json
  {
    "amount": 250.5,
    "type": "buy",
    "asset_id": 1
  }
  ```
- **Successful Response (201 Created)**: Returns the newly created transaction object.
- **Error Responses**:
  - `404 Not Found`: If the `asset_id` does not exist or does not belong to the user.
  - `400 Bad Request`: If attempting to sell more than the asset's current value.
- **How to Test (cURL)**:
  ```bash
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  # Assumes an asset with id=1 exists for this user
  curl -X 'POST' \
    'http://127.0.0.1:8000/transactions/' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
    -H 'Content-Type: application/json' \
    -d '{
      "amount": 250.50,
      "type": "buy",
      "asset_id": 1,
      "to_user_id": 2
    }'
  ```

---

### Reports (`/reports`)

Endpoint for generating high-level summary reports.

#### **Get Platform-Wide Report**

- **Purpose**: Provides a summary report of key metrics for the entire platform. This is intended for administrative overview.
- **Endpoint**: `GET /reports/`
- **Authentication**: Required (Bearer Token)
- **Successful Response (200 OK)**: A JSON object containing platform-wide statistics like total assets, total value, transaction distributions, and the single most valuable asset on the platform.
- **How to Test (cURL)**:
  ```bash
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  curl -X 'GET' \
    'http://127.0.0.1:8000/reports/' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
  ```

---

### Analytics (`/analytics`)

Endpoint for retrieving structured data suitable for creating graphs and visualizations.

#### **Get Platform-Wide Graph Data**

- **Purpose**: Provides time-series and categorical data for the entire platform, suitable for plotting graphs.
- **Endpoint**: `GET /analytics/graphs`
- **Authentication**: Required (Bearer Token)
- **Query Parameters**:
  - `start_date` (string, optional, format: YYYY-MM-DD): The start date for filtering time-series data.
  - `end_date` (string, optional, format: YYYY-MM-DD): The end date for filtering time-series data.
- **Successful Response (200 OK)**: A JSON object with keys for different metrics (`user_growth`, `transaction_volume`, etc.), each containing arrays of dates and corresponding values.
- **Error Responses**:
  - `400 Bad Request`: If `start_date` is after `end_date`.
- **How to Test (cURL)**:

  ```bash
  # Without date filters
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  curl -X 'GET' \
    'http://127.0.0.1:8000/analytics/graphs' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'

  # With date filters
  # Replace <YOUR_ACCESS_TOKEN> with your actual token
  curl -X 'GET' \
    'http://127.0.0.1:8000/analytics/graphs?start_date=2023-01-01&end_date=2023-12-31' \
    -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
  ```
