# SOC-X

SOC-X is a starting point for a security operations platform with a FastAPI backend, Linux telemetry collector, detection layer, and frontend.

## Structure

- `backend/app`: API application, database access, models, schemas, routes, and services
- `collector`: host telemetry collectors
- `detection`: detection rules and analysis logic
- `frontend`: web client
- `tests`: automated tests

## Run the API

```powershell
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API health check is available at `http://127.0.0.1:8000/health`.

## Run tests

From the project root:

```powershell
python -m pytest
```
