from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import List, Optional, Dict, Any

from app.models.fund import (
    MutualFund,
    FundSectorAllocation,
    FundStockAllocation,
    FundMarketCapAllocation,
    FundOverlap,
    FundHolding
)
from app.models.investment import UserInvestment
from app.schemas.fund import MutualFundCreate


def get_fund(db: Session, fund_id: int) -> Optional[MutualFund]:
    return db.query(MutualFund).filter(MutualFund.id == fund_id).first()


def get_fund_by_isn(db: Session, isn: str) -> Optional[MutualFund]:
    return db.query(MutualFund).filter(MutualFund.isn == isn).first()


def get_funds(db: Session, skip: int = 0, limit: int = 100) -> List[MutualFund]:
    return db.query(MutualFund).offset(skip).limit(limit).all()


def create_fund(db: Session, fund: MutualFundCreate) -> MutualFund:
    db_fund = MutualFund(
        name=fund.name,
        fund_type=fund.fund_type,
        isn=fund.isn,
        nav=fund.nav
    )
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund


def update_fund(db: Session, fund_id: int, fund: MutualFundCreate) -> Optional[MutualFund]:
    db_fund = get_fund(db, fund_id)
    if not db_fund:
        return None

    for field, value in fund.dict().items():
        setattr(db_fund, field, value)

    db.commit()
    db.refresh(db_fund)
    return db_fund


def delete_fund(db: Session, fund_id: int) -> bool:
    db_fund = get_fund(db, fund_id)
    if not db_fund:
        return False

    db.delete(db_fund)
    db.commit()
    return True


def get_portfolio_sector_allocation(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Get sector allocation for a user's portfolio"""
    # Get user investments with current values
    investments = db.query(
        UserInvestment.fund_id,
        (UserInvestment.units * MutualFund.nav).label("current_value")
    ).join(
        MutualFund, UserInvestment.fund_id == MutualFund.id
    ).filter(
        UserInvestment.user_id == user_id
    ).all()

    if not investments:
        return []

    # Calculate total portfolio value
    total_value = sum(inv.current_value for inv in investments)

    # Create a dictionary of fund weights in the portfolio
    fund_weights = {inv.fund_id: inv.current_value / total_value for inv in investments}

    # Get sector allocations for all funds in the portfolio
    sector_allocations = db.query(
        FundSectorAllocation.fund_id,
        FundSectorAllocation.sector,
        FundSectorAllocation.percentage
    ).filter(
        FundSectorAllocation.fund_id.in_([inv.fund_id for inv in investments])
    ).all()

    # Calculate weighted sector allocations
    sector_values = {}
    for alloc in sector_allocations:
        weight = fund_weights.get(alloc.fund_id, 0)
        sector = alloc.sector
        value = weight * (alloc.percentage / 100) * total_value

        if sector in sector_values:
            sector_values[sector] += value
        else:
            sector_values[sector] = value

    # Format result
    result = []
    for sector, amount in sector_values.items():
        percentage = (amount / total_value) * 100
        result.append({
            "sector": sector,
            "amount": round(amount, 2),
            "percentage": round(percentage, 2)
        })

    # Sort by amount descending
    result.sort(key=lambda x: x["amount"], reverse=True)

    return result


def get_fund_overlap(db: Session, fund1_id: int, fund2_id: int) -> Optional[Dict[str, Any]]:
    """Get overlap details between two funds"""
    overlap = db.query(FundOverlap).filter(
        or_(
            and_(FundOverlap.fund_id_1 == fund1_id, FundOverlap.fund_id_2 == fund2_id),
            and_(FundOverlap.fund_id_1 == fund2_id, FundOverlap.fund_id_2 == fund1_id)
        )
    ).first()

    if not overlap:
        return None

    # Get fund names
    fund1 = get_fund(db, fund1_id)
    fund2 = get_fund(db, fund2_id)

    return {
        "fund_id_1": overlap.fund_id_1,
        "fund_id_2": overlap.fund_id_2,
        "fund_name_1": fund1.name if fund1 else "Unknown",
        "fund_name_2": fund2.name if fund2 else "Unknown",
        "overlap_percentage": overlap.overlap_percentage,
        "overlapping_stocks": overlap.overlapping_stocks
    }


def get_all_fund_overlaps(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Get all fund overlaps for funds in a user's portfolio"""
    # Get funds in user's portfolio
    user_funds = db.query(UserInvestment.fund_id).filter(
        UserInvestment.user_id == user_id
    ).distinct().all()

    user_fund_ids = [f.fund_id for f in user_funds]

    if len(user_fund_ids) < 2:
        return []

    # Get all overlaps between these funds
    overlaps = db.query(FundOverlap).filter(
        and_(
            FundOverlap.fund_id_1.in_(user_fund_ids),
            FundOverlap.fund_id_2.in_(user_fund_ids)
        )
    ).all()

    # Get fund names
    funds = {f.id: f.name for f in db.query(MutualFund.id, MutualFund.name).filter(
        MutualFund.id.in_(user_fund_ids)
    ).all()}

    # Format result
    result = []
    for overlap in overlaps:
        result.append({
            "fund_id_1": overlap.fund_id_1,
            "fund_id_2": overlap.fund_id_2,
            "fund_name_1": funds.get(overlap.fund_id_1, "Unknown"),
            "fund_name_2": funds.get(overlap.fund_id_2, "Unknown"),
            "overlap_percentage": overlap.overlap_percentage,
            "overlapping_stocks": overlap.overlapping_stocks
        })

    return result