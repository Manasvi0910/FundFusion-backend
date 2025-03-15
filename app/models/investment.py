from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class UserInvestment(Base):
    __tablename__ = "user_investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    investment_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    nav_at_investment = Column(Float, nullable=False)
    units = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="investments")
    fund = relationship("MutualFund", back_populates="investments")