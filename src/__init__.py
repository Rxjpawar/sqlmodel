from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is Starting")
    await init_db()
    yield
    print("Server is shutting down")

version = "v1"

app  = FastAPI(
    title = "my app",
    version = version,
    description="sql model app",
    lifespan=lifespan
)

app.include_router(book_router,prefix=f"/api/{version}/books",tags=["books"])
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=['auth'])