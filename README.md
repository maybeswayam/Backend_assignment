# EaseOps E-Library Backend

The user-facing API backend for the EaseOps progressive web app (PWA) e-library platform.

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** Supabase (PostgreSQL)
- **Authentication:** JWT (`python-jose`), `bcrypt` for password hashing
- **Validation:** Pydantic

## Features

- **Auth:** Registration, login, and secure JWT-based token refresh flows.
- **Users:** Read and update user profiles, toggle UI preferences like dark mode.
- **Library:** Retrieve e-book catalogs, filter by category/tags, and search.
- **Reading:** Save and manage bookmarks and personal notes for individual e-books.
- **Interactions:** Submit platform feedback, answer surveys, and list FAQs.

## Prerequisites

- Python 3.10+
- `pip`
- A Supabase account and project

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone <repo_url>
   cd easeops-elibrary-backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```


## Running the Server

Start the development server using uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## API Documentation

FastAPI autogenerates interactive API documentation. Once the server is running, visit:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### Auth

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/auth/register` | Register a new user and generate initial tokens |
| `POST` | `/auth/login` | Authenticate user and return access & refresh tokens |
| `POST` | `/auth/refresh` | Validate refresh token and return a new access token |

### Users

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/users/me` | Fetch the current logged-in user's profile |
| `PATCH` | `/users/me` | Update name or email |
| `PATCH` | `/users/preferences` | Update UI preferences (e.g., dark mode) |

### Library

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/library/ebooks` | List all e-books, supports `?category=` and `?tag=` |
| `GET` | `/library/ebooks/{id}` | Get single e-book details incl. file/cover URL |
| `GET` | `/library/search` | Search by title or metadata via `?q=` |
| `GET` | `/library/categories` | List all unique categories |

### Reading

| Method | Route | Description | Auth Required |
| --- | --- | --- | --- |
| `POST` | `/reading/bookmarks` | Add a bookmark for an e-book | Yes |
| `GET` | `/reading/bookmarks` | Get user bookmarks (requires `?ebook_id=`) | Yes |
| `DELETE` | `/reading/bookmarks/{id}` | Remove a bookmark | Yes |
| `POST` | `/reading/notes` | Add a note to a specific page | Yes |
| `GET` | `/reading/notes` | Get user notes (requires `?ebook_id=`) | Yes |
| `DELETE` | `/reading/notes/{id}` | Remove a note | Yes |

### Interactions

| Method | Route | Description |
| --- | --- | --- | --- |
| `POST` | `/interactions/feedback` | Submit feedback or contact request |
| `POST` | `/interactions/surveys` | Submit JSON responses to a survey |
| `GET` | `/interactions/faqs` | Fetch a list of FAQs |

## Database Tables

1. **users**: Stores user credentials, email, and core preferences.
2. **ebooks**: E-book metadata (title, author, tags, file URLs).
3. **bookmarks**: Tracks user bookmarks tied to specific e-books and page numbers.
4. **notes**: Personal user notes tied to specific e-book pages.
5. **feedback**: General platform feedback submitted by users.
6. **surveys**: JSONB-based survey responses from users.
7. **faqs**: Frequently asked questions displayed to users.

---
