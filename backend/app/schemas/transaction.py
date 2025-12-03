from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.category import Category

class TransactionBase(BaseModel):
    category_id: int
    amount: float
    description: Optional[str] = None
    date: date
    type: str  # "income" or "expense"

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None
    type: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    category: Optional[Category] = None

    class Config:
        from_attributes = True

