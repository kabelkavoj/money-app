from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Float, nullable=False)  # Positive for income, negative for expenses
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)  # "income", "expense", or "transfer"
    
    # Bank account relationships
    from_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)  # For expenses and transfers (money going out)
    to_account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=True)  # For income and transfers (money coming in)
    
    # Relationships
    category = relationship("Category", backref="transactions")
    from_account = relationship("BankAccount", foreign_keys=[from_account_id], backref="outgoing_transactions")
    to_account = relationship("BankAccount", foreign_keys=[to_account_id], backref="incoming_transactions")

