from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta

from app.models.investment import UserInvestment
from app.models.fund import MutualFund, HistoricalNAV
from app.schemas.investment import InvestmentCreate, FundPerformance


def get_investment(db: Session, investment_id: int) -> Optional[UserInvestment]:
    return db.query(UserInvestment).filter(UserInvestment.id == investment_id).first()


def get_user_investments(db: Session, user_id: int) -> List[UserInvestment]:
    return db.query(UserInvestment).filter(UserInvestment.user_id == user_id).all()


def create_investment(db: Session, investment: InvestmentCreate) -> UserInvestment:
    # Calculate units based on amount and NAV
    units = investment.amount / investment.nav_at_investment

    db_investment = UserInvestment(
        user_id=investment.user_id,
        fund_id=investment.fund_id,
        investment_date=investment.investment_date,
        amount=investment.amount,
        nav_at_investment=investment.nav_at_investment,
        units=units
    )
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment


def update_investment(db: Session, investment_id: int, investment: InvestmentCreate) -> Optional[UserInvestment]:
    db_investment = get_investment(db, investment_id)
    if not db_investment:
        return None

    # Calculate new units if amount or NAV changed
    if investment.amount != db_investment.amount or investment.nav_at_investment != db_investment.nav_at_investment:
        units = investment.amount / investment.nav_at_investment
        setattr(db_investment, "units", units)

    for field, value in investment.dict(exclude={"units"}).items():
        setattr(db_investment, field, value)

    db.commit()
    db.refresh(db_investment)
    return db_investment


def delete_investment(db: Session, investment_id: int) -> bool:
    db_investment = get_investment(db, investment_id)
    if not db_investment:
        return False

    db.delete(db_investment)
    db.commit()
    return True


def get_investment_summary(db: Session, user_id: int) -> Tuple[float, float]:
    """Calculate current and initial investment value for a user"""
    result = db.query(
        func.sum(UserInvestment.units * MutualFund.nav).label("current_value"),
        func.sum(UserInvestment.amount).label("initial_value")
    ).join(
        MutualFund, UserInvestment.fund_id == MutualFund.id
    ).filter(
        UserInvestment.user_id == user_id
    ).first()

    return result.current_value or 0.0, result.initial_value or 0.0


def get_performance_extremes(db: Session, user_id: int) -> Tuple[FundPerformance, FundPerformance]:
    """Get best and worst performing funds for a user"""
    query = db.query(
        MutualFund.id,
        MutualFund.name,
        ((MutualFund.nav - UserInvestment.nav_at_investment) / UserInvestment.nav_at_investment * 100).label(
            "return_percentage")
    ).join(
        UserInvestment, UserInvestment.fund_id == MutualFund.id
    ).filter(
        UserInvestment.user_id == user_id
    )

    # Best performing fund
    best_fund = query.order_by(desc("return_percentage")).first()

    # Worst performing fund
    worst_fund = query.order_by("return_percentage").first()

    if not best_fund or not worst_fund:
        # Default values if no funds found
        empty_fund = {"id": 0, "name": "N/A", "return_percentage": 0.0}
        return empty_fund, empty_fund

    best_fund_dict = {
        "id": best_fund.id,
        "name": best_fund.name,
        "return_percentage": round(best_fund.return_percentage, 2)
    }

    worst_fund_dict = {
        "id": worst_fund.id,
        "name": worst_fund.name,
        "return_percentage": round(worst_fund.return_percentage, 2)
    }

    return best_fund_dict, worst_fund_dict


def get_historical_performance(db: Session, user_id: int, period: str = "1M") -> List[Dict[str, Any]]:
    """
    Get historical performance data for line chart with optimized query performance.
    Using a single SQL query with proper joins and sampling for longer periods.
    """
    # Determine date range based on period
    today = datetime.now().date()
    if period == "1M":
        start_date = today - timedelta(days=30)
        # For a month, get daily data
        interval = 'day'
    elif period == "3M":
        start_date = today - timedelta(days=90)
        # For 3 months, get data every 2 days
        interval = 'day'
        sampling_factor = 2
    elif period == "6M":
        start_date = today - timedelta(days=180)
        # For 6 months, get data every 3 days
        interval = 'day'
        sampling_factor = 3
    elif period == "1Y":
        start_date = today - timedelta(days=365)
        # For 1 year, get weekly data
        interval = 'week'
    elif period == "3Y":
        start_date = today - timedelta(days=1095)
        # For 3 years, get bi-weekly data
        interval = 'week'
        sampling_factor = 2
    else:  # MAX
        start_date = today - timedelta(days=3650)  # 10 years
        # For MAX, get monthly data
        interval = 'month'

    # Build the base query with interval sampling for date
    if interval == 'day' and period in ["3M", "6M"]:
        # For day intervals with sampling, manually select dates
        # at the specified sampling rate
        date_query = db.query(
            HistoricalNAV.date
        ).filter(
            HistoricalNAV.date >= start_date,
            HistoricalNAV.date <= today
        ).group_by(
            HistoricalNAV.date
        ).order_by(
            HistoricalNAV.date
        )

        # Apply sampling for longer periods to reduce data points
        if period == "3M":
            # Keep every 2nd day
            dates = [row.date for i, row in enumerate(date_query) if i % 2 == 0]
        elif period == "6M":
            # Keep every 3rd day
            dates = [row.date for i, row in enumerate(date_query) if i % 3 == 0]
        else:
            dates = [row.date for row in date_query]

        # Do the actual query with the sampled dates
        query = db.query(
            HistoricalNAV.date,
            func.sum(UserInvestment.units * HistoricalNAV.nav).label("portfolio_value")
        ).join(
            UserInvestment, HistoricalNAV.fund_id == UserInvestment.fund_id
        ).filter(
            UserInvestment.user_id == user_id,
            HistoricalNAV.date.in_(dates),
            UserInvestment.investment_date <= HistoricalNAV.date
        ).group_by(
            HistoricalNAV.date
        ).order_by(
            HistoricalNAV.date
        )

    else:
        # For week/month intervals, use PostgreSQL's date_trunc function
        # This is much more efficient than manual sampling
        query = db.query(
            func.date_trunc(interval, HistoricalNAV.date).label('grouped_date'),
            func.avg(UserInvestment.units * HistoricalNAV.nav).label("avg_value")
        ).join(
            UserInvestment, HistoricalNAV.fund_id == UserInvestment.fund_id
        ).filter(
            UserInvestment.user_id == user_id,
            HistoricalNAV.date >= start_date,
            HistoricalNAV.date <= today,
            UserInvestment.investment_date <= HistoricalNAV.date
        ).group_by(
            'grouped_date'
        ).order_by(
            'grouped_date'
        )

        if interval == 'week' and period == "3Y":
            # For 3Y, get every other week
            result_all = query.all()
            result = [row for i, row in enumerate(result_all) if i % 2 == 0]
        else:
            result = query.all()

        # Format the result
        return [
            {
                "date": row.grouped_date.strftime("%d %b") if hasattr(row, 'grouped_date') else row.date.strftime(
                    "%d %b"),
                "value": round(row.avg_value if hasattr(row, 'avg_value') else row.portfolio_value, 2)
            }
            for row in result
        ]

    # Execute query
    result = query.all()

    # Format result
    performance_data = [
        {
            "date": row.date.strftime("%d %b"),
            "value": round(row.portfolio_value, 2)
        }
        for row in result
    ]

    return performance_data