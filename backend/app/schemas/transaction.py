from datetime import date
from typing import Optional

from pydantic import BaseModel, model_validator

from app.schemas.category import Category
from app.schemas.bank_account import BankAccount

class TransactionBase(BaseModel):
    category_id: int
    amount: float
    description: Optional[str] = None
    date: date
    type: str  # "income", "expense", or "transfer"
    from_account_id: Optional[int] = None  # For expenses and transfers (money going out)
    to_account_id: Optional[int] = None  # For income and transfers (money coming in)

class TransactionCreate(TransactionBase):
    @model_validator(mode='after')
    def validate_accounts(self):
        """Validate that at least one account is set and accounts match transaction type"""
        if self.type == "income":
            if not self.to_account_id:
                raise ValueError("to_account_id is required for income transactions")
            if self.from_account_id:
                raise ValueError("from_account_id should not be set for income transactions")
        elif self.type == "expense":
            if not self.from_account_id:
                raise ValueError("from_account_id is required for expense transactions")
            if self.to_account_id:
                raise ValueError("to_account_id should not be set for expense transactions")
        elif self.type == "transfer":
            if not self.from_account_id or not self.to_account_id:
                raise ValueError("Both from_account_id and to_account_id are required for transfer transactions")
            if self.from_account_id == self.to_account_id:
                raise ValueError("from_account_id and to_account_id must be different for transfers")
        else:
            raise ValueError(f"Invalid transaction type: {self.type}. Must be 'income', 'expense', or 'transfer'")
        return self

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None
    type: Optional[str] = None
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None

class Transaction(TransactionBase):
    id: int
    category: Optional[Category] = None
    from_account: Optional[BankAccount] = None
    to_account: Optional[BankAccount] = None

    class Config:
        from_attributes = True

