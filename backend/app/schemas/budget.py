from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.category import Category

class BudgetBase(BaseModel):
    category_id: int
    amount: float
    period: str  # "monthly", "yearly"
    start_date: date
    end_date: Optional[date] = None

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    period: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class Budget(BudgetBase):
    id: int
    category: Optional[Category] = None

    class Config:
        from_attributes = True

