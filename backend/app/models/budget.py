from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Float, nullable=False)  # Budgeted amount
    period = Column(String, nullable=False)  # "monthly", "yearly", etc.
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    
    # Relationship
    category = relationship("Category", backref="budgets")

