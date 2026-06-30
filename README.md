# CORS Handling in FastAPI

This repository demonstrates how to configure and handle **Cross-Origin Resource Sharing (CORS)** in a FastAPI backend application, allowing it to securely communicate with a frontend client (like React running on `http://localhost:5173`) that is served from a different origin.

This version has been updated to load environment and configuration parameters dynamically using an `.env` file and a centralized configuration settings loader.

---

## Table of Contents
1. [What is CORS?](#what-is-cors)
2. [Prerequisites](#prerequisites)
3. [Environment Configuration (`.env`)](#environment-configuration-env)
4. [Centralized Configuration (`config.py`)](#centralized-configuration-configpy)
5. [How CORS is Configured in FastAPI (`main.py`)](#how-cors-is-configured-in-fastapi-mainpy)
6. [Backend CORS Middleware Parameters Explained](#backend-cors-middleware-parameters-explained)
7. [Running the Backend](#running-the-backend)
8. [How Frontend Connects to the Backend](#how-frontend-connects-to-the-backend)

---

## What is CORS?

**Cross-Origin Resource Sharing (CORS)** is a security mechanism implemented by web browsers to restrict web pages from making requests to a different domain than the one that served the web page. 

An **origin** is defined by the combination of:
*   **Protocol** (e.g., `http` vs `https`)
*   **Domain / Host** (e.g., `localhost` vs `127.0.0.1` vs `example.com`)
*   **Port** (e.g., `:5173` vs `:8000`)

Since your frontend (running on `http://localhost:5173`) is on a different origin than your backend API (running on `http://127.0.0.1:8000`), the browser will block requests by default unless the backend explicitly declares that it permits requests from the frontend's origin.

---

## Prerequisites

To run the backend, ensure you have Python 3.7+ installed along with the required libraries, including `python-dotenv` for loading environment variables:

```bash
pip install fastapi uvicorn python-dotenv
```

---

## Environment Configuration (`.env`)

Create a `.env` file in the root directory of your project to store environment-specific variables:

```env
SECRET_KEY = "mysecret"
origins = [
    "http://localhost:5173"
]
DB_URL = sqllite:///.test.db 
```

*   **`origins`**: Specifies the frontend application's origin that is allowed to interact with the backend API.
*   **`SECRET_KEY`**: A secret key used for signing cryptographic tokens or sessions.
*   **`DB_URL`**: The database connection string (e.g., SQLite filepath).

---

## Centralized Configuration (`config.py`)

The application loads environment variables using the `dotenv` package and defines a structured `Settings` class to make them available across the app:

```python
import os 
from dotenv import load_dotenv

load_dotenv() # Read .env file for environment variables

class Settings:
    # Allow origins for frontend url 
    origins = os.getenv("origins")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_URL = os.getenv("DB_URL")

settings = Settings()
```

---

## How CORS is Configured in FastAPI (`main.py`)

In FastAPI, CORS is handled using the built-in `CORSMiddleware`. We import the initialized `settings` from `config.py` to fetch our allowed origins dynamically:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI()

# Add CORSMiddleware to the application using settings.origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins, # Allow frontend url from settings
    allow_credentials=True,         # Allow cookies, authorization headers, etc.
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allow all custom headers
)

@app.get('/')
def home():
    return {
        "message": "CORS Enable API"        
    }
```

---

## Backend CORS Middleware Parameters Explained

When setting up `CORSMiddleware`, the following options control access:

*   **`allow_origins`**: A list of origins that are allowed to make cross-origin requests. 
    *   *Example:* `["http://localhost:5173"]` allows only your frontend dev server.
    *   *Caution:* You can use `["*"]` to allow all origins, but this is **not recommended** in production if you are using credentials.
*   **`allow_credentials`**: Indicates whether the request can include credentials such as cookies, HTTP authentication, or SSL client certificates. Must be a boolean (`True`/`False`).
*   **`allow_methods`**: A list of HTTP methods that should be allowed for cross-origin requests. 
    *   Use `["*"]` to allow all standard methods (e.g., `GET`, `POST`, `PUT`, `DELETE`, `PATCH`).
*   **`allow_headers`**: A list of HTTP request headers that should be supported. 
    *   Use `["*"]` to allow all headers, or specify list entries (e.g. `["Content-Type", "Authorization"]`).

---

## Running the Backend

To start the FastAPI backend server, run the following command from the project root directory:

```bash
uvicorn main:app --reload
```

*   `main` refers to the Python file name (`main.py`).
*   `app` refers to the `FastAPI` instance created inside `main.py`.
*   `--reload` enables auto-reloading so the server restarts whenever you modify the code.

Once started, the backend API documentation will be available at:
*   Swagger UI Docs: `http://127.0.0.1:8000/docs`
*   ReDoc: `http://127.0.0.1:8000/redoc`

---

## How Frontend Connects to the Backend

1.  **Request Origin**: When the frontend client (running on `http://localhost:5173`) performs a `fetch` or `axios` call to the backend URL (e.g., `http://127.0.0.1:8000/`):
    ```javascript
    fetch('http://127.0.0.1:8000/')
      .then(res => res.json())
      .then(data => console.log(data))
    ```
2.  **Origin Checking**: The browser automatically appends an `Origin: http://localhost:5173` header to the request.
3.  **Backend Verification & Handshake**:
    *   For safe requests (like basic `GET` requests without special headers), the server responds with `Access-Control-Allow-Origin: http://localhost:5173`.
    *   For unsafe or complex requests (like `POST` with JSON payloads, or requests with custom headers), the browser first sends an automatic **preflight request** using the `OPTIONS` method. The backend must approve this preflight request based on the configured `CORSMiddleware` before the actual request is sent.
4.  **Successful Response**: If the origin is in the allowed list (`origins`), the browser allows the frontend application to read the response. If it's not, a CORS policy error is thrown in the browser console.
