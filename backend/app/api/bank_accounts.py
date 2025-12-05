from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.bank_account import BankAccount
from app.models.user import User
from app.schemas.bank_account import BankAccount as BankAccountSchema, BankAccountCreate, BankAccountUpdate

router = APIRouter()

@router.get("/", response_model=List[BankAccountSchema])
def get_bank_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bank accounts"""
    accounts = db.query(BankAccount).offset(skip).limit(limit).all()
    return accounts

@router.get("/{account_id}", response_model=BankAccountSchema)
def get_bank_account(account_id: int, db: Session = Depends(get_db)):
    """Get a specific bank account"""
    account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return account

@router.post("/", response_model=BankAccountSchema)
def create_bank_account(account: BankAccountCreate, db: Session = Depends(get_db)):
    """Create a new bank account"""
    # Verify owner exists
    owner = db.query(User).filter(User.id == account.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_account = BankAccount(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.put("/{account_id}", response_model=BankAccountSchema)
def update_bank_account(account_id: int, account: BankAccountUpdate, db: Session = Depends(get_db)):
    """Update a bank account"""
    db_account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    # Verify owner if being updated
    if account.owner_id is not None:
        owner = db.query(User).filter(User.id == account.owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail="User not found")
    
    update_data = account.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/{account_id}")
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    """Delete a bank account"""
    db_account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    db.delete(db_account)
    db.commit()
    return {"message": "Bank account deleted successfully"}

