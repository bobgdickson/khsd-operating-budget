# khsd-operating-budget

FastAPI application for CRUD operations on an operating budget table.

## Configuration

Create a `.env` file from the example and set your database URL:

```bash
cp .env.example .env
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the app

```bash
uvicorn app.main:app --reload
```

Access the HTMX-powered UI at <http://127.0.0.1:8000/>

## Testing

```bash
pytest
```