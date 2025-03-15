from app.crud.user import get_user, get_user_by_email, get_users, create_user, update_user, delete_user
from app.crud.investment import (
    get_investment,
    get_user_investments,
    create_investment,
    update_investment,
    delete_investment,
    get_investment_summary,
    get_performance_extremes,
    get_historical_performance
)
from app.crud.fund import (
    get_fund,
    get_fund_by_isn,
    get_funds,
    create_fund,
    update_fund,
    delete_fund,
    get_portfolio_sector_allocation,
    get_fund_overlap,
    get_all_fund_overlaps
)