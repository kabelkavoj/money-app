from pydantic import BaseModel
from typing import Optional
from app.schemas.user import User

class BankAccountBase(BaseModel):
    name: str
    currency: str = "USD"
    initial_balance: float = 0.0
    current_balance: float = 0.0
    owner_id: int

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[str] = None
    initial_balance: Optional[float] = None
    current_balance: Optional[float] = None
    owner_id: Optional[int] = None

class BankAccount(BankAccountBase):
    id: int
    owner: Optional["User"] = None

    class Config:
        from_attributes = True

