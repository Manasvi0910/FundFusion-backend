from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class MutualFund(Base):
    __tablename__ = "mutual_funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fund_type = Column(String, nullable=False)
    isn = Column(String, unique=True, nullable=False)
    nav = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    investments = relationship("UserInvestment", back_populates="fund")
    sector_allocations = relationship("FundSectorAllocation", back_populates="fund")
    stock_allocations = relationship("FundStockAllocation", back_populates="fund")
    market_cap_allocations = relationship("FundMarketCapAllocation", back_populates="fund")
    historical_navs = relationship("HistoricalNAV", back_populates="fund")
    holdings = relationship("FundHolding", back_populates="fund")


class FundSectorAllocation(Base):
    __tablename__ = "fund_sector_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    sector = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    fund = relationship("MutualFund", back_populates="sector_allocations")


class FundStockAllocation(Base):
    __tablename__ = "fund_stock_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    stock_name = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    fund = relationship("MutualFund", back_populates="stock_allocations")


class FundMarketCapAllocation(Base):
    __tablename__ = "fund_market_cap_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    cap_type = Column(String, nullable=False)  # Large Cap, Mid Cap, Small Cap
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    fund = relationship("MutualFund", back_populates="market_cap_allocations")


class FundOverlap(Base):
    __tablename__ = "fund_overlaps"

    id = Column(Integer, primary_key=True, index=True)
    fund_id_1 = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    fund_id_2 = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    overlap_percentage = Column(Float, nullable=False)
    overlapping_stocks = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('fund_id_1', 'fund_id_2', name='unique_fund_pair'),
    )


class HistoricalNAV(Base):
    __tablename__ = "historical_nav"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    date = Column(Date, nullable=False)
    nav = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    fund = relationship("MutualFund", back_populates="historical_navs")

    __table_args__ = (
        UniqueConstraint('fund_id', 'date', name='unique_fund_date'),
    )


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    holdings = relationship("FundHolding", back_populates="stock")


class FundHolding(Base):
    __tablename__ = "fund_holdings"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    fund = relationship("MutualFund", back_populates="holdings")
    stock = relationship("Stock", back_populates="holdings")

    __table_args__ = (
        UniqueConstraint('fund_id', 'stock_id', name='unique_fund_stock'),
    )