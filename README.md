# backend-intern-crud

FastAPI implementation for LawVriksh **Assignment 1: Blog Post CRUD with Like & Comment**, including JWT auth and a Postman collection.

## Quickstart

```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# optional: export env vars
export JWT_SECRET="change-me"  # Windows PowerShell: $Env:JWT_SECRET="change-me"

uvicorn src.app:app --reload
```

API root: `http://127.0.0.1:8000`  
Docs: `http://127.0.0.1:8000/docs`

### Test flow (high level)
1. **Sign up** → `/api/auth/signup`
2. **Login** (get JWT) → `/api/auth/login`
3. **Create Post** (Bearer token) → `/api/posts`
4. **List Posts** → `/api/posts`
5. **Like Post** → `/api/posts/{id}/like`
6. **Comment on Post** → `/api/posts/{id}/comment`
7. **Get Comments** → `/api/posts/{id}/comments`

### Repo structure
```
src/
  app.py
  database.py
  models.py
  schemas.py
  auth.py
  deps.py
  routers/
    auth.py
    posts.py
```

### Postman
Import `postman_collection.json` and run requests (authorized vs unauthorized examples included).

### Notes
- Protected write operations: create/update/delete/like/comment require JWT.
- A user cannot like the same post more than once; endpoint is idempotent.
