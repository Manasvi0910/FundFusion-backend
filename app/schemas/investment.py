from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional, Dict, Any


class InvestmentBase(BaseModel):
    fund_id: int
    investment_date: date
    amount: float
    nav_at_investment: float


class InvestmentCreate(InvestmentBase):
    user_id: int


class Investment(InvestmentBase):
    id: int
    user_id: int
    units: float
    fund_name: Optional[str] = None
    current_value: Optional[float] = None
    return_percentage: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True


class PerformanceData(BaseModel):
    date: str
    value: float


class FundPerformance(BaseModel):
    id: int
    name: str
    return_percentage: float


class DashboardData(BaseModel):
    user_name: str
    current_investment_value: float
    initial_investment_value: float
    best_performing_scheme: FundPerformance
    worst_performing_scheme: FundPerformance
    performance_data: List[PerformanceData]
    sector_allocation: List[Dict[str, Any]]
    fund_overlap: List[Dict[str, Any]]

    class Config:
        orm_mode = True