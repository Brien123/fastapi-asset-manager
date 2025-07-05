# Codexbase Network API

This is the backend API for the Codexbase Network hiring process, built with FastAPI. It provides a comprehensive solution for managing users, financial assets, and transactions, along with reporting and analytics features.

## Features

* **User Authentication**: Secure user registration and JWT-based authentication.
* **Asset Management**: Create and list financial assets (Stocks, Crypto, Real Estate).
* **Transaction Tracking**: Log buy, sell, and transfer transactions, with automatic asset value updates.
* **Paginated Responses**: Efficiently browse large sets of data for assets and users.
* **Reporting & Analytics**: Endpoints for generating summary reports and data for graphical visualization.
* **Interactive API Docs**: Automatic, interactive API documentation powered by Swagger UI.

## Technology Stack

* **Backend**: Python 3
* **Framework**: FastAPI
* **Database**: SQLAlchemy with SQLite
* **Data Validation**: Pydantic
* **Authentication**: JWT with Passlib for password hashing

## Project Setup

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites

* Python 3.9+, preferably python 3.12
* A virtual environment tool (`venv`)

### 2. Clone the Repository

```bash
git clone https://github.com/Brien123/fastapi-asset-manager.git
cd fastapi-asset-manager
```

### 3. Set Up Virtual Environment

Create and activate a virtual environment.

**On macOS and Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy the example environment file. The `SECRET_KEY` is used for encoding JWTs.

```bash
cp .env.example .env
```

Open the `.env` file and set your `SECRET_KEY`. You can generate a strong secret key using Python:
`python -c 'import secrets; print(secrets.token_hex(32))'`. The default key is fine though.

### 6. Run the Application (Local)

Start the development server using Uvicorn.

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running the Application with Docker

Alternatively, you can build and run the project using Docker:

```bash
docker build -t codexbase .
docker run -d -p 8000:8000 codexbase
```

The API will be accessible at `http://localhost:8000`.

## Interactive API Documentation

Once the server is running, you can access the interactive API documentation in your browser at `http://127.0.0.1:8000/docs`.

This UI allows you to test all API endpoints directly from your browser.

## First Step: Create a User

Before using any authenticated routes, create a user using the `/users` route. Example request body:

```json
{
  "username": "test",
  "email": "test@test.com",
  "password": "12345678"
}
```

### Authorizing in the Docs

To access protected endpoints that show a lock icon, you need to authorize your session:

1. Click the **"Authorize"** button located at the top right of the page.
2. In the popup, enter the `username` and `password` of the registered user you created into the form and click the "Authorize" button within the popup.
3. Close the popup. The UI will now automatically include your authorization token in requests to protected routes.

### Using External Clients (Postman, cURL)

If you prefer to use an external API client, you need to manually acquire and use the JWT token:

1. Make a `POST` request to the `/auth/` endpoint with a JSON body containing your `username` and `password`.
2. The API will respond with an `access_token`.
3. For all subsequent requests to protected endpoints, include this token in the `Authorization` header as a Bearer token:

   ```
   Authorization: Bearer <your_access_token>
   ```

## API Endpoints Overview

Here is a summary of the available API endpoints.

### Authentication (`/auth`)

* **`POST /auth/token`**: Authenticates a user and returns a JWT access token.

### Users (`/users`)

* **`POST /users/`**: Creates a new user.
* **`GET /users/`**: Lists all users (requires authentication).

### Assets (`/assets`)

* **`POST /assets/`**: Creates a new asset for the authenticated user.

  * **Sample Body**:

    ```json
    {
      "name": "Bitcoin",
      "type": "crypto",
      "value": 65000.00
    }
    ```
* **`GET /assets/`**: Lists all assets for the authenticated user with pagination.

### Transactions (`/transactions`)

* **`POST /transactions/`**: Creates a new transaction and updates the corresponding asset's value.

  * **Sample Body**:

    ```json
    {
      "amount": 1000,
      "type": "buy",
      "asset_id": 1
    }
    ```

### Reports & Analytics

* **`GET /reports/`**: Provides a summary report for the authenticated user.
* **`GET /analytics/graphs`**: Provides structured data ready for plotting graphs.
