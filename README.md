# Wallet API

REST API for personal finance tracking: create wallets, add income and expenses, check balances.

## Tech stack

- Python 3.12+
- FastAPI
- Pydantic v2: request validation
- SQLAlchemy 2.1 (ORM)
- PostgreSQL (psycopg 3 driver)

## Project structure

```
├── api/v1/            # FastAPI routers (HTTP layer)
│   ├── wallets.py
│   └── operations.py
├── service/           # business logic: checks, error handling
│   ├── wallets.py
│   └── operations.py
├── repository/        # database access via SQLAlchemy
│   └── wallets.py
├── models.py          # Wallet ORM model
├── schemas.py         # Pydantic request schemas
├── database.py        # DB connection, sessions
└── hh.py              # entry point, app creation
```

A request goes through the layers: `api` → `service` → `repository` → DB.

## Getting started

1. Clone the repository and create a virtual environment:

```bash
git clone https://github.com/TeHbBaXyi/wallet_api.git
cd wallet_api
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a PostgreSQL database and a `.env` file in the project root:

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/wallet
```

3. Run the server:

```bash
uvicorn hh:app --reload
```

Tables are created automatically on startup. Swagger docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path | Description |
|-------|------|----------|
| POST | `/api/v1/wallet` | Create a wallet |
| GET | `/api/v1/balance` | Total balance of all wallets |
| GET | `/api/v1/balance?wallet_name=...` | Balance of a single wallet |
| POST | `/api/v1/operations/income` | Add income |
| POST | `/api/v1/operations/expense` | Add expense |

### Examples

Create a wallet:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/wallet \
  -H "Content-Type: application/json" \
  -d '{"name": "card", "initial_balance": 1000}'
```

```json
{"message": "Wallet card created", "wallet": "card", "balance": 1000}
```

Add an expense:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/operations/expense \
  -H "Content-Type: application/json" \
  -d '{"wallet_name": "card", "amount": 250, "description": "Groceries"}'
```

```json
{"message": "Expense added", "wallet": "card", "amount": 250, "description": "Groceries", "new_balance": 750}
```

## Validation and errors

- Wallet name must not be empty, max 25 characters.
- Operation amount must be positive; initial balance cannot be negative.
- Money is stored as `Decimal` to avoid floating-point errors.

| Code | When |
|-----|-------|
| 400 | Wallet with this name already exists; insufficient funds |
| 404 | Wallet not found |
| 422 | Invalid input (Pydantic validation error) |

## Roadmap

- [ ] Operation history (separate table)
- [ ] Alembic migrations
- [ ] Tests (pytest + TestClient)
- [ ] Docker and docker-compose
