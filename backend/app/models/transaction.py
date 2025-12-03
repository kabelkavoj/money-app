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
    type = Column(String, nullable=False)  # "income" or "expense"
    
    # Relationship
    category = relationship("Category", backref="transactions")

