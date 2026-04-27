# Tasks Manager REST API

A production-ready REST API for managing tasks, built with Python and Flask. Supports full CRUD operations, status/priority filtering, interactive Swagger documentation, and is deployable on Render with PostgreSQL.

## Features

- **Full CRUD** — Create, read, update, and delete tasks
- **Filtering** — Filter tasks by `status` or `priority` via query parameters
- **Swagger UI** — Interactive API documentation at `/docs`
- **PostgreSQL support** — Render-compatible with automatic `postgres://` URL fix
- **SQLite for local dev** — Zero-configuration local development
- **Input validation** — Request validation via Marshmallow schemas

## Tech Stack

| Layer      | Technology                                     |
|------------|------------------------------------------------|
| Language   | Python 3.11+                                   |
| Framework  | Flask 3                                        |
| ORM        | Flask-SQLAlchemy                               |
| Validation | Marshmallow + Flask-Smorest                    |
| Database   | SQLite (development) / PostgreSQL (production) |
| Server     | Gunicorn                                       |

## API Endpoints

| Method   | Endpoint             | Description                                        |
|----------|----------------------|----------------------------------------------------|
| `GET`    | `/`                  | Health check                                       |
| `GET`    | `/docs`              | Swagger UI                                         |
| `GET`    | `/api/v1/tasks`      | List all tasks (`?status=` & `?priority=` filters) |
| `POST`   | `/api/v1/tasks`      | Create a new task                                  |
| `GET`    | `/api/v1/tasks/{id}` | Get a task by ID                                   |
| `PUT`    | `/api/v1/tasks/{id}` | Update a task                                      |
| `DELETE` | `/api/v1/tasks/{id}` | Delete a task                                      |

### Task Fields

| Field         | Type   | Values                                    | Default    |
|---------------|--------|-------------------------------------------|------------|
| `title`       | string | max 200 characters, required              | —          |
| `description` | string | any text, optional                        | null       |
| `status`      | string | `pending` \| `in_progress` \| `done`      | `pending`  |
| `priority`    | string | `low` \| `medium` \| `high`               | `medium`   |

## Local Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd tasks-manager-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your settings if needed

# 5. Run the development server
python app.py
```

The API will be available at `http://localhost:5000`  
Swagger UI will be available at `http://localhost:5000/docs`

### Example Request

```bash
# Create a task
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Build portfolio project", "priority": "high"}'

# List tasks filtered by status
curl "http://localhost:5000/api/v1/tasks?status=pending"
```

## Deployment (Render)

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn app:app`
5. Add environment variables from `.env.example` in the Render dashboard
6. Set `DATABASE_URL` to your Render PostgreSQL connection string

## Live Demo

> Coming soon

## License

[MIT](LICENSE)

## Author

Ahmed Raslan
