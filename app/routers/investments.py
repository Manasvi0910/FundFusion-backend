from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Investment)
def create_investment(investment: schemas.InvestmentCreate, db: Session = Depends(get_db)):
    return crud.create_investment(db=db, investment=investment)


@router.get("/user/{user_id}", response_model=List[schemas.Investment])
def read_user_investments(user_id: int, db: Session = Depends(get_db)):
    investments = crud.get_user_investments(db, user_id=user_id)
    return investments


@router.get("/{investment_id}", response_model=schemas.Investment)
def read_investment(investment_id: int, db: Session = Depends(get_db)):
    db_investment = crud.get_investment(db, investment_id=investment_id)
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found")
    return db_investment


@router.put("/{investment_id}", response_model=schemas.Investment)
def update_investment(investment_id: int, investment: schemas.InvestmentCreate, db: Session = Depends(get_db)):
    db_investment = crud.update_investment(db, investment_id=investment_id, investment=investment)
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found")
    return db_investment


@router.delete("/{investment_id}", response_model=bool)
def delete_investment(investment_id: int, db: Session = Depends(get_db)):
    result = crud.delete_investment(db, investment_id=investment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Investment not found")
    return result


@router.get("/dashboard/{user_id}", response_model=schemas.DashboardData)
def get_dashboard_data(user_id: int, db: Session = Depends(get_db)):
    """Get dashboard summary data for a specific user"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get investment summary
    current_value, initial_value = crud.get_investment_summary(db, user_id=user_id)

    # Get best and worst performing funds
    best_fund, worst_fund = crud.get_performance_extremes(db, user_id=user_id)

    # Get historical performance data
    performance_data = crud.get_historical_performance(db, user_id=user_id, period="1M")

    # Get sector allocation data
    sector_allocation = crud.get_portfolio_sector_allocation(db, user_id=user_id)

    # Get fund overlap data
    fund_overlap = crud.get_all_fund_overlaps(db, user_id=user_id)

    return {
        "user_name": user.name,
        "current_investment_value": current_value,
        "initial_investment_value": initial_value,
        "best_performing_scheme": best_fund,
        "worst_performing_scheme": worst_fund,
        "performance_data": performance_data,
        "sector_allocation": sector_allocation,
        "fund_overlap": fund_overlap
    }