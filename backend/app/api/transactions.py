from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.bank_account import BankAccount
from app.schemas.transaction import Transaction as TransactionSchema, TransactionCreate, TransactionUpdate

router = APIRouter()

def update_account_balance(account_id: int, amount: float, db: Session):
    """Update a bank account's current balance"""
    account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
    if account:
        account.current_balance += amount
        db.commit()
        return account
    return None

def reverse_transaction_effect(transaction: Transaction, db: Session):
    """Reverse the effect of a transaction on bank account balances"""
    if transaction.type == "income" and transaction.to_account_id:
        # Reverse: subtract the amount
        update_account_balance(transaction.to_account_id, -abs(transaction.amount), db)
    elif transaction.type == "expense" and transaction.from_account_id:
        # Reverse: add back the amount (expense was negative)
        update_account_balance(transaction.from_account_id, abs(transaction.amount), db)
    elif transaction.type == "transfer":
        if transaction.from_account_id:
            # Reverse: add back to source account
            update_account_balance(transaction.from_account_id, abs(transaction.amount), db)
        if transaction.to_account_id:
            # Reverse: subtract from destination account
            update_account_balance(transaction.to_account_id, -abs(transaction.amount), db)

def apply_transaction_effect(transaction: Transaction, db: Session):
    """Apply the effect of a transaction on bank account balances"""
    if transaction.type == "income" and transaction.to_account_id:
        # Income: add to account
        update_account_balance(transaction.to_account_id, abs(transaction.amount), db)
    elif transaction.type == "expense" and transaction.from_account_id:
        # Expense: subtract from account (amount is already negative)
        update_account_balance(transaction.from_account_id, transaction.amount, db)
    elif transaction.type == "transfer":
        if transaction.from_account_id:
            # Transfer: subtract from source account
            update_account_balance(transaction.from_account_id, -abs(transaction.amount), db)
        if transaction.to_account_id:
            # Transfer: add to destination account
            update_account_balance(transaction.to_account_id, abs(transaction.amount), db)

@router.get("/", response_model=List[TransactionSchema])
def get_transactions(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get all transactions with optional filters"""
    query = db.query(Transaction)
    
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=TransactionSchema)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=TransactionSchema)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == transaction.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Verify bank accounts exist
    if transaction.from_account_id:
        from_account = db.query(BankAccount).filter(BankAccount.id == transaction.from_account_id).first()
        if not from_account:
            raise HTTPException(status_code=404, detail="Source bank account not found")
    
    if transaction.to_account_id:
        to_account = db.query(BankAccount).filter(BankAccount.id == transaction.to_account_id).first()
        if not to_account:
            raise HTTPException(status_code=404, detail="Destination bank account not found")
    
    # Ensure amount sign matches type
    if transaction.type == "expense" and transaction.amount > 0:
        transaction.amount = -abs(transaction.amount)
    elif transaction.type == "income" and transaction.amount < 0:
        transaction.amount = abs(transaction.amount)
    elif transaction.type == "transfer":
        # Transfers should always be positive (we'll handle the sign in balance updates)
        transaction.amount = abs(transaction.amount)
    
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Update bank account balances
    apply_transaction_effect(db_transaction, db)
    
    return db_transaction

@router.put("/{transaction_id}", response_model=TransactionSchema)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    """Update a transaction"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Verify category if being updated
    if transaction.category_id is not None:
        category = db.query(Category).filter(Category.id == transaction.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Verify bank accounts if being updated
    if transaction.from_account_id is not None:
        from_account = db.query(BankAccount).filter(BankAccount.id == transaction.from_account_id).first()
        if not from_account:
            raise HTTPException(status_code=404, detail="Source bank account not found")
    
    if transaction.to_account_id is not None:
        to_account = db.query(BankAccount).filter(BankAccount.id == transaction.to_account_id).first()
        if not to_account:
            raise HTTPException(status_code=404, detail="Destination bank account not found")
    
    # Reverse the old transaction effect before updating
    reverse_transaction_effect(db_transaction, db)
    
    update_data = transaction.model_dump(exclude_unset=True)
    
    # Handle amount sign based on type
    if "type" in update_data or "amount" in update_data:
        trans_type = update_data.get("type", db_transaction.type)
        amount = update_data.get("amount", db_transaction.amount)
        if trans_type == "expense" and amount > 0:
            update_data["amount"] = -abs(amount)
        elif trans_type == "income" and amount < 0:
            update_data["amount"] = abs(amount)
        elif trans_type == "transfer":
            update_data["amount"] = abs(amount)
    
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.commit()
    db.refresh(db_transaction)
    
    # Apply the new transaction effect
    apply_transaction_effect(db_transaction, db)
    
    return db_transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Reverse the transaction effect on bank account balances
    reverse_transaction_effect(db_transaction, db)
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

