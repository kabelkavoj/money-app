from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import budgets, categories, transactions
# Import all models to ensure they're registered with Base.metadata for table creation
from app.models import Category, Budget, Transaction, User, BankAccount  # noqa: F401

# Create database tables (only creates tables that don't exist - safe to call multiple times)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Family Money App API",
    description="API for family budgeting and financial tracking",
    version="1.0.0"
)

# CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(budgets.router, prefix="/api/budgets", tags=["budgets"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Family Money App API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

