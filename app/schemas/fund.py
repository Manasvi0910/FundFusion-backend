from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any


class MutualFundBase(BaseModel):
    name: str
    fund_type: str
    isn: str
    nav: float


class MutualFundCreate(MutualFundBase):
    pass


class MutualFund(MutualFundBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SectorAllocation(BaseModel):
    sector: str
    amount: float
    percentage: float


class StockAllocation(BaseModel):
    stock_name: str
    percentage: float


class MarketCapAllocation(BaseModel):
    cap_type: str
    percentage: float


class FundOverlap(BaseModel):
    fund_id_1: int
    fund_id_2: int
    fund_name_1: Optional[str] = None
    fund_name_2: Optional[str] = None
    overlap_percentage: float
    overlapping_stocks: int

    class Config:
        orm_mode = True