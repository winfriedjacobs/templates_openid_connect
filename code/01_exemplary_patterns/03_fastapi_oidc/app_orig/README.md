# FastAPI Keycloak Auth Application

This is a FastAPI application with Keycloak authentication. The project is configured to be started using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) installed

## Installation

1. Install uv if you haven't already:

```bash
pip install uv
```

2. Clone this repository and navigate to the project directory:

```bash
git clone <repository-url>
cd app
```

3. Install the project dependencies using uv:

```bash
uv pip install -e .
```

## Running the Application

The project includes two scripts defined in the `pyproject.toml` file:

### Start the application

To start the application using the main.py file:

```bash
uv run start
```

This will start the application on http://0.0.0.0:8000.

### Development mode

To run the application in development mode with auto-reload:

```bash
uv run dev
```

This will start the application using Uvicorn directly with the reload option enabled.

## Project Structure

- `main.py`: The entry point of the application
- `src/`: Contains the application code
  - `main.py`: Creates and configures the FastAPI application
  - `routes/`: Contains the route handlers
  - `auth.py`: Authentication-related functionality
  - `config.py`: Application configuration

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc