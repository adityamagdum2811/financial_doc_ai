from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth_routes, document_routes, role_routes, rag_routes
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(auth_routes.router)
app.include_router(document_routes.router)
app.include_router(role_routes.router)
app.include_router(rag_routes.router)


@app.get("/")
def root():
    return {"message": "Financial Document Management API is running"}