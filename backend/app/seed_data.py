"""
Script to seed initial data for development/testing.
Run this after setting up the database to get started with some sample data.
"""
from datetime import date, timedelta

from app.database import SessionLocal, engine, Base
from app.models.category import Category
from app.models.budget import Budget
from app.models.transaction import Transaction
from app.models.user import User
from app.models.bank_account import BankAccount

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if data already exists
    if db.query(Category).count() > 0 or db.query(User).count() > 0:
        print("Database already has data. Skipping seed.")
        exit(0)
    
    # Create users first (needed for bank accounts)
    print("Creating users...")
    users = [
        User(username="john_doe", email="john@example.com", full_name="John Doe"),
        User(username="jane_smith", email="jane@example.com", full_name="Jane Smith"),
    ]
    
    for user in users:
        db.add(user)
    db.commit()
    
    print(f"Created {len(users)} users")
    
    # Get user IDs for bank accounts
    john = db.query(User).filter(User.username == "john_doe").first()
    jane = db.query(User).filter(User.username == "jane_smith").first()

    # Create categories
    categories = [
        Category(name="Groceries", description="Food and household items", color="#3B82F6", icon="🛒"),
        Category(name="Transportation", description="Gas, public transport, car maintenance", color="#10B981", icon="🚗"),
        Category(name="Utilities", description="Electricity, water, internet", color="#F59E0B", icon="💡"),
        Category(name="Entertainment", description="Movies, dining out, hobbies", color="#EF4444", icon="🎬"),
        Category(name="Healthcare", description="Medical expenses, insurance", color="#8B5CF6", icon="🏥"),
        Category(name="Income", description="Salary and other income", color="#10B981", icon="💰"),
    ]

    for category in categories:
        db.add(category)
    db.commit()

    print(f"Created {len(categories)} categories")

    # Get category IDs
    groceries = db.query(Category).filter(Category.name == "Groceries").first()
    transportation = db.query(Category).filter(Category.name == "Transportation").first()
    utilities = db.query(Category).filter(Category.name == "Utilities").first()
    entertainment = db.query(Category).filter(Category.name == "Entertainment").first()
    income = db.query(Category).filter(Category.name == "Income").first()

    # Create budgets
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    
    budgets = [
        Budget(category_id=groceries.id, amount=600.0, period="monthly", start_date=start_of_month),
        Budget(category_id=transportation.id, amount=300.0, period="monthly", start_date=start_of_month),
        Budget(category_id=utilities.id, amount=200.0, period="monthly", start_date=start_of_month),
        Budget(category_id=entertainment.id, amount=150.0, period="monthly", start_date=start_of_month),
    ]

    for budget in budgets:
        db.add(budget)
    db.commit()

    print(f"Created {len(budgets)} budgets")

    # Create sample transactions
    transactions = [
        # Income
        Transaction(category_id=income.id, amount=5000.0, description="Salary", date=start_of_month, type="income"),
        
        # Expenses
        Transaction(category_id=groceries.id, amount=-150.0, description="Weekly groceries", date=start_of_month + timedelta(days=2), type="expense"),
        Transaction(category_id=groceries.id, amount=-120.0, description="Weekly groceries", date=start_of_month + timedelta(days=9), type="expense"),
        Transaction(category_id=groceries.id, amount=-180.0, description="Weekly groceries", date=start_of_month + timedelta(days=16), type="expense"),
        
        Transaction(category_id=transportation.id, amount=-60.0, description="Gas", date=start_of_month + timedelta(days=5), type="expense"),
        Transaction(category_id=transportation.id, amount=-45.0, description="Gas", date=start_of_month + timedelta(days=18), type="expense"),
        
        Transaction(category_id=utilities.id, amount=-85.0, description="Electricity", date=start_of_month + timedelta(days=10), type="expense"),
        Transaction(category_id=utilities.id, amount=-45.0, description="Internet", date=start_of_month + timedelta(days=10), type="expense"),
        
        Transaction(category_id=entertainment.id, amount=-75.0, description="Dinner out", date=start_of_month + timedelta(days=7), type="expense"),
        Transaction(category_id=entertainment.id, amount=-30.0, description="Movie tickets", date=start_of_month + timedelta(days=14), type="expense"),
    ]

    for transaction in transactions:
        db.add(transaction)
    db.commit()

    print(f"Created {len(transactions)} transactions")
    
    # Create bank accounts
    print("\nCreating bank accounts...")
    bank_accounts = [
        BankAccount(
            name="John's Checking",
            currency="USD",
            initial_balance=5000.0,
            current_balance=5000.0,
            owner_id=john.id
        ),
        BankAccount(
            name="John's Savings",
            currency="USD",
            initial_balance=10000.0,
            current_balance=10000.0,
            owner_id=john.id
        ),
        BankAccount(
            name="Jane's Checking",
            currency="USD",
            initial_balance=3000.0,
            current_balance=3000.0,
            owner_id=jane.id
        ),
        BankAccount(
            name="Jane's EUR Account",
            currency="EUR",
            initial_balance=2000.0,
            current_balance=2000.0,
            owner_id=jane.id
        ),
    ]
    
    for account in bank_accounts:
        db.add(account)
    db.commit()
    
    print(f"Created {len(bank_accounts)} bank accounts")
    
    print("\n✅ Seed data created successfully!")
    print("\nYou can now:")
    print("1. Start the backend: cd backend && uvicorn app.main:app --reload")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Visit http://localhost:5173 to see your app!")

except Exception as e:
    print(f"Error seeding data: {e}")
    db.rollback()
finally:
    db.close()

