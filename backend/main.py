from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.api.v1.api import api_router
from app.api.v1.endpoints.admin import seed_demo_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and auto-seed statutory tax rules and demo persona
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_database(db)
    finally:
        db.close()
    yield
    # Shutdown logic if any

app = FastAPI(
    title="TaxClaim AI — Intelligent Tax Evidence Platform",
    description="Evidence-backed, explainable, jurisdiction-aware tax intelligence platform for freelancers & gig workers.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "TaxClaim AI Intelligence Engine",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
