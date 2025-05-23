
# Flask User API

A lightweight, containerized Flask backend providing JWT-protected CRUD operations on a simple User model, complete with Swagger documentation, automated tests, and CI/CD via GitHub Actions.

---

## 📝 Overview

This project demonstrates how to build, test, document, and deploy a small Flask application end-to-end:

- **REST API** for Create, Read, Delete on Users  
- **JWT Authentication** (via `flask-jwt-extended`)  
- **SQLAlchemy ORM** with SQLite (or override via `DATABASE_URL`)  
- **Swagger UI** (via `flask-restx`) at `/docs`  
- **Docker** containerization  
- **Automated tests** (pytest) & linting (flake8)  
- **CI pipeline** (GitHub Actions) on pushes to `main`

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
cd <YOUR-REPO-NAME>
````

### 2. Environment variables

Create a `.env` (or set in your shell/CI) with:

```bash
SECRET_KEY="your-flask-secret"
JWT_SECRET_KEY="your-jwt-secret"
DATABASE_URL="sqlite:///app.db"    # or your Postgres/MySQL URL
```

> On Docker, we’ll pass these via `-e` flags.

---

## 🛠️ Local Development

1. **Create & activate** a virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows (PowerShell)
   ```

2. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Initialize database & run**

   ```bash
   python app.py
   ```

   The app will be available at `http://127.0.0.1:5000/`.
   Swagger UI → `http://127.0.0.1:5000/docs`

---

## 🐳 Docker

1. **Build the image**

   ```bash
   docker build -t flask-user-api .
   ```

2. **Run the container**

   ```bash
   docker run -d \
     --name user-api \
     -p 5000:5000 \
     -e SECRET_KEY="$SECRET_KEY" \
     -e JWT_SECRET_KEY="$JWT_SECRET_KEY" \
     -e DATABASE_URL="$DATABASE_URL" \
     flask-user-api
   ```

3. **Verify**

   ```bash
   curl http://localhost:5000/docs
   ```

   You should see the Swagger UI HTML.

---

## 📚 API Documentation

Browse live docs & “Try it out” at

```
http://localhost:5000/docs
```

Endpoints:

| Method | Path          | Description        | Auth Required |
| ------ | ------------- | ------------------ | ------------- |
| POST   | `/login`      | Obtain a JWT token | No            |
| GET    | `/users/`     | List all users     | Yes           |
| POST   | `/users/`     | Create a new user  | Yes           |
| GET    | `/users/{id}` | Get user by ID     | Yes           |
| DELETE | `/users/{id}` | Delete user by ID  | Yes           |

> **Authorize:** click 🔒 in the top-right of `/docs`, paste `Bearer <your-token>`.

---

## ✅ Testing

Run unit & integration tests with pytest:

```bash
pytest --maxfail=1 --disable-warnings -q
```

Ensure all tests under `tests/` pass before committing.

---

## 🔄 CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) will automatically:

1. Check out your code
2. Set up Python 3.9
3. Install dependencies & dev tools
4. Lint with flake8
5. Run pytest

Push to `main` to trigger the pipeline.

---

## 📂 Project Structure

```
├── app.py                     # Flask application & route definitions
├── config.py                  # Centralized configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container build recipe
├── .github/
│   └── workflows/ci.yml       # CI pipeline definition
└── tests/
    └── test_app.py            # pytest-based unit & integration tests
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/XYZ`)
3. Commit your changes & push (`git push origin feature/XYZ`)
4. Open a Pull Request—ensure CI passes

---



