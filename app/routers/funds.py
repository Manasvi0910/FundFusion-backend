from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.MutualFund)
def create_fund(fund: schemas.MutualFundCreate, db: Session = Depends(get_db)):
    db_fund = crud.get_fund_by_isn(db, isn=fund.isn)
    if db_fund:
        raise HTTPException(status_code=400, detail="Fund with this ISN already exists")
    return crud.create_fund(db=db, fund=fund)


@router.get("/", response_model=List[schemas.MutualFund])
def read_funds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    funds = crud.get_funds(db, skip=skip, limit=limit)
    return funds


@router.get("/{fund_id}", response_model=schemas.MutualFund)
def read_fund(fund_id: int, db: Session = Depends(get_db)):
    db_fund = crud.get_fund(db, fund_id=fund_id)
    if db_fund is None:
        raise HTTPException(status_code=404, detail="Fund not found")
    return db_fund


@router.put("/{fund_id}", response_model=schemas.MutualFund)
def update_fund(fund_id: int, fund: schemas.MutualFundCreate, db: Session = Depends(get_db)):
    db_fund = crud.update_fund(db, fund_id=fund_id, fund=fund)
    if db_fund is None:
        raise HTTPException(status_code=404, detail="Fund not found")
    return db_fund


@router.delete("/{fund_id}", response_model=bool)
def delete_fund(fund_id: int, db: Session = Depends(get_db)):
    result = crud.delete_fund(db, fund_id=fund_id)
    if not result:
        raise HTTPException(status_code=404, detail="Fund not found")
    return result