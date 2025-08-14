from fastapi import FastAPI
from .database import Base, engine
from .routers import auth as auth_router, posts as posts_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LawVriksh Blog API")

app.include_router(auth_router.router)
app.include_router(posts_router.router)

@app.get("/", tags=["root"])
def root():
    return {"ok": True, "service": "LawVriksh Blog API"}
