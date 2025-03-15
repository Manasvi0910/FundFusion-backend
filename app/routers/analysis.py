from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.get("/sector-allocation/{user_id}", response_model=List[schemas.SectorAllocation])
def get_sector_allocation(user_id: int, db: Session = Depends(get_db)):
    """Get sector allocation for a user's portfolio"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_portfolio_sector_allocation(db, user_id=user_id)


@router.get("/overlap/{user_id}", response_model=List[schemas.FundOverlap])
def get_overlap_analysis(
        user_id: int,
        fund1_id: Optional[int] = None,
        fund2_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """Get overlap analysis for funds in user's portfolio"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if fund1_id and fund2_id:
        # Get overlap for specific funds
        overlap = crud.get_fund_overlap(db, fund1_id=fund1_id, fund2_id=fund2_id)
        if not overlap:
            raise HTTPException(status_code=404, detail="Overlap data not found")
        return [overlap]
    else:
        # Get all overlaps for user's funds
        return crud.get_all_fund_overlaps(db, user_id=user_id)