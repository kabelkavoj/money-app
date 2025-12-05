from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import budgets, categories, transactions, bank_accounts, users

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
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(bank_accounts.router, prefix="/api/bank-accounts", tags=["bank-accounts"])

@app.get("/")
async def root():
    return {"message": "Family Money App API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

