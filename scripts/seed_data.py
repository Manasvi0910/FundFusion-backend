#!/usr/bin/env python3
"""
Seed script to populate the database with initial data for development and testing.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    User,
    MutualFund,
    UserInvestment,
    FundSectorAllocation,
    FundStockAllocation,
    FundMarketCapAllocation,
    FundOverlap,
    HistoricalNAV,
    Stock,
    FundHolding
)

# Create tables
Base.metadata.create_all(bind=engine)


# Seed data
def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        print("Seeding database...")

        # Create users
        user1 = User(name="Yashna", email="yashna@example.com")
        db.add(user1)
        db.commit()
        db.refresh(user1)

        # Create mutual funds
        funds = [
            MutualFund(name="ICICI Prudential Bluechip Fund", fund_type="Large Cap", isn="INF109K016L0", nav=112.50),
            MutualFund(name="HDFC Top 100 Fund", fund_type="Large Cap", isn="INF179K01YV8", nav=110.20),
            MutualFund(name="SBI Bluechip Fund", fund_type="Large Cap", isn="INF200K01QX4", nav=111.00),
            MutualFund(name="Axis Bluechip Fund", fund_type="Large Cap", isn="INF846K01DP8", nav=95.00),
            MutualFund(name="Mirae Asset Large Cap Fund", fund_type="Large Cap", isn="INF769K01AX2", nav=113.00),
            MutualFund(name="ICICI Prudential Midcap Fund", fund_type="Mid Cap", isn="INF109K01BL2", nav=119.00),
            MutualFund(name="Axis Flexi Cap Fund", fund_type="Flexi Cap", isn="INF846K01CH9", nav=95.00),
            MutualFund(name="Motilal Large Cap Fund - Direct Plan", fund_type="Large Cap", isn="INF247L01AJ8",
                       nav=105.00),
            MutualFund(name="Nippon Large Cap Fund - Direct Plan", fund_type="Large Cap", isn="INF204K01CP3",
                       nav=108.00),
            MutualFund(name="HDFC Large Cap Fund", fund_type="Large Cap", isn="INF179K01CQ2", nav=106.00),
        ]
        db.add_all(funds)
        db.commit()
        for fund in funds:
            db.refresh(fund)

        # Create user investments
        investments = [
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[0].id,
                investment_date=datetime(2023, 1, 10).date(),
                amount=1000000.0,
                nav_at_investment=100.0,
                units=10000.0
            ),
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[1].id,
                investment_date=datetime(2022, 12, 5).date(),
                amount=800000.0,
                nav_at_investment=100.0,
                units=8000.0
            ),
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[2].id,
                investment_date=datetime(2023, 2, 15).date(),
                amount=1200000.0,
                nav_at_investment=100.0,
                units=12000.0
            ),
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[3].id,
                investment_date=datetime(2022, 11, 20).date(),
                amount=950000.0,
                nav_at_investment=100.0,
                units=9500.0
            ),
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[4].id,
                investment_date=datetime(2023, 3, 1).date(),
                amount=1100000.0,
                nav_at_investment=100.0,
                units=11000.0
            ),
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[5].id,
                investment_date=datetime(2023, 2, 1).date(),
                amount=600000.0,
                nav_at_investment=100.0,
                units=6000.0
            ),
            UserInvestment(
                user_id=user1.id,
                fund_id=funds[6].id,
                investment_date=datetime(2023, 1, 15).date(),
                amount=700000.0,
                nav_at_investment=100.0,
                units=7000.0
            ),
        ]
        db.add_all(investments)
        db.commit()

        # Create sector allocations
        sector_allocations = [
            # ICICI Prudential Bluechip Fund
            FundSectorAllocation(fund_id=funds[0].id, sector="Technology", percentage=38.0),
            FundSectorAllocation(fund_id=funds[0].id, sector="Financial", percentage=37.0),
            FundSectorAllocation(fund_id=funds[0].id, sector="Energy", percentage=25.0),

            # HDFC Top 100 Fund
            FundSectorAllocation(fund_id=funds[1].id, sector="Financial", percentage=80.0),
            FundSectorAllocation(fund_id=funds[1].id, sector="Energy", percentage=20.0),

            # SBI Bluechip Fund
            FundSectorAllocation(fund_id=funds[2].id, sector="Technology", percentage=40.0),
            FundSectorAllocation(fund_id=funds[2].id, sector="Financial", percentage=21.0),
            FundSectorAllocation(fund_id=funds[2].id, sector="Energy", percentage=27.0),
            FundSectorAllocation(fund_id=funds[2].id, sector="Industrials", percentage=12.0),

            # Axis Bluechip Fund
            FundSectorAllocation(fund_id=funds[3].id, sector="Technology", percentage=50.0),
            FundSectorAllocation(fund_id=funds[3].id, sector="Financial", percentage=32.0),
            FundSectorAllocation(fund_id=funds[3].id, sector="Energy", percentage=18.0),

            # Mirae Asset Large Cap Fund
            FundSectorAllocation(fund_id=funds[4].id, sector="Technology", percentage=42.0),
            FundSectorAllocation(fund_id=funds[4].id, sector="Financial", percentage=34.0),
            FundSectorAllocation(fund_id=funds[4].id, sector="Energy", percentage=24.0),

            # ICICI Prudential Midcap Fund
            FundSectorAllocation(fund_id=funds[5].id, sector="Technology", percentage=30.0),
            FundSectorAllocation(fund_id=funds[5].id, sector="Financial", percentage=25.0),
            FundSectorAllocation(fund_id=funds[5].id, sector="Healthcare", percentage=20.0),
            FundSectorAllocation(fund_id=funds[5].id, sector="Consumer Goods", percentage=15.0),
            FundSectorAllocation(fund_id=funds[5].id, sector="Industrials", percentage=10.0),

            # Axis Flexi Cap Fund
            FundSectorAllocation(fund_id=funds[6].id, sector="Technology", percentage=35.0),
            FundSectorAllocation(fund_id=funds[6].id, sector="Financial", percentage=25.0),
            FundSectorAllocation(fund_id=funds[6].id, sector="Healthcare", percentage=20.0),
            FundSectorAllocation(fund_id=funds[6].id, sector="Consumer Goods", percentage=10.0),
            FundSectorAllocation(fund_id=funds[6].id, sector="Energy", percentage=10.0),

            # Motilal Large Cap Fund
            FundSectorAllocation(fund_id=funds[7].id, sector="Technology", percentage=45.0),
            FundSectorAllocation(fund_id=funds[7].id, sector="Financial", percentage=35.0),
            FundSectorAllocation(fund_id=funds[7].id, sector="Energy", percentage=20.0),

            # Nippon Large Cap Fund
            FundSectorAllocation(fund_id=funds[8].id, sector="Technology", percentage=40.0),
            FundSectorAllocation(fund_id=funds[8].id, sector="Financial", percentage=30.0),
            FundSectorAllocation(fund_id=funds[8].id, sector="Energy", percentage=20.0),
            FundSectorAllocation(fund_id=funds[8].id, sector="Consumer Goods", percentage=10.0),

            # HDFC Large Cap Fund
            FundSectorAllocation(fund_id=funds[9].id, sector="Financial", percentage=60.0),
            FundSectorAllocation(fund_id=funds[9].id, sector="Energy", percentage=25.0),
            FundSectorAllocation(fund_id=funds[9].id, sector="Technology", percentage=15.0),
        ]
        db.add_all(sector_allocations)
        db.commit()

        # Create stocks
        stocks = [
            Stock(symbol="RELIANCE", name="Reliance Industries", sector="Energy"),
            Stock(symbol="HDFCBANK", name="HDFC Bank", sector="Financial"),
            Stock(symbol="TCS", name="Tata Consultancy Services", sector="Technology"),
            Stock(symbol="INFY", name="Infosys", sector="Technology"),
            Stock(symbol="ICICIBANK", name="ICICI Bank", sector="Financial"),
            Stock(symbol="KOTAKBANK", name="Kotak Mahindra Bank", sector="Financial"),
            Stock(symbol="BAJFINANCE", name="Bajaj Finance", sector="Financial"),
            Stock(symbol="LT", name="Larsen & Toubro", sector="Industrials"),
            Stock(symbol="SBI", name="State Bank of India", sector="Financial"),
            Stock(symbol="BHARTIARTL", name="Bharti Airtel", sector="Telecom"),
            Stock(symbol="HINDUNILVR", name="Hindustan Unilever", sector="Consumer Goods"),
            Stock(symbol="ASIANPAINT", name="Asian Paints", sector="Consumer Goods"),
            Stock(symbol="SUNPHARMA", name="Sun Pharmaceutical", sector="Healthcare"),
            Stock(symbol="DRREDDY", name="Dr. Reddy's Laboratories", sector="Healthcare"),
            Stock(symbol="CIPLA", name="Cipla", sector="Healthcare"),
        ]
        db.add_all(stocks)
        db.commit()
        for stock in stocks:
            db.refresh(stock)

        # Create fund holdings
        holdings = [
            # ICICI Prudential Bluechip Fund
            FundHolding(fund_id=funds[0].id, stock_id=stocks[0].id, percentage=25.0),
            FundHolding(fund_id=funds[0].id, stock_id=stocks[1].id, percentage=22.0),
            FundHolding(fund_id=funds[0].id, stock_id=stocks[2].id, percentage=20.0),
            FundHolding(fund_id=funds[0].id, stock_id=stocks[3].id, percentage=18.0),
            FundHolding(fund_id=funds[0].id, stock_id=stocks[4].id, percentage=15.0),

            # HDFC Top 100 Fund
            FundHolding(fund_id=funds[1].id, stock_id=stocks[1].id, percentage=28.0),
            FundHolding(fund_id=funds[1].id, stock_id=stocks[4].id, percentage=24.0),
            FundHolding(fund_id=funds[1].id, stock_id=stocks[0].id, percentage=20.0),
            FundHolding(fund_id=funds[1].id, stock_id=stocks[5].id, percentage=18.0),
            FundHolding(fund_id=funds[1].id, stock_id=stocks[6].id, percentage=10.0),

            # SBI Bluechip Fund
            FundHolding(fund_id=funds[2].id, stock_id=stocks[0].id, percentage=27.0),
            FundHolding(fund_id=funds[2].id, stock_id=stocks[2].id, percentage=23.0),
            FundHolding(fund_id=funds[2].id, stock_id=stocks[1].id, percentage=21.0),
            FundHolding(fund_id=funds[2].id, stock_id=stocks[3].id, percentage=17.0),
            FundHolding(fund_id=funds[2].id, stock_id=stocks[7].id, percentage=12.0),

            # Axis Bluechip Fund
            FundHolding(fund_id=funds[3].id, stock_id=stocks[2].id, percentage=26.0),
            FundHolding(fund_id=funds[3].id, stock_id=stocks[3].id, percentage=24.0),
            FundHolding(fund_id=funds[3].id, stock_id=stocks[1].id, percentage=22.0),
            FundHolding(fund_id=funds[3].id, stock_id=stocks[0].id, percentage=18.0),
            FundHolding(fund_id=funds[3].id, stock_id=stocks[8].id, percentage=10.0),

            # Mirae Asset Large Cap Fund
            FundHolding(fund_id=funds[4].id, stock_id=stocks[0].id, percentage=24.0),
            FundHolding(fund_id=funds[4].id, stock_id=stocks[1].id, percentage=23.0),
            FundHolding(fund_id=funds[4].id, stock_id=stocks[2].id, percentage=22.0),
            FundHolding(fund_id=funds[4].id, stock_id=stocks[3].id, percentage=20.0),
            FundHolding(fund_id=funds[4].id, stock_id=stocks[4].id, percentage=11.0),
        ]
        db.add_all(holdings)
        db.commit()

        # Create fund overlaps
        overlaps = [
            FundOverlap(fund_id_1=funds[0].id, fund_id_2=funds[1].id, overlap_percentage=67.0, overlapping_stocks=3),
            FundOverlap(fund_id_1=funds[0].id, fund_id_2=funds[2].id, overlap_percentage=87.0, overlapping_stocks=4),
            FundOverlap(fund_id_1=funds[0].id, fund_id_2=funds[3].id, overlap_percentage=88.0, overlapping_stocks=4),
            FundOverlap(fund_id_1=funds[0].id, fund_id_2=funds[4].id, overlap_percentage=100.0, overlapping_stocks=5),
            FundOverlap(fund_id_1=funds[1].id, fund_id_2=funds[2].id, overlap_percentage=48.0, overlapping_stocks=2),
            FundOverlap(fund_id_1=funds[1].id, fund_id_2=funds[3].id, overlap_percentage=44.0, overlapping_stocks=2),
            FundOverlap(fund_id_1=funds[1].id, fund_id_2=funds[4].id, overlap_percentage=65.0, overlapping_stocks=3),
            FundOverlap(fund_id_1=funds[2].id, fund_id_2=funds[3].id, overlap_percentage=89.0, overlapping_stocks=4),
            FundOverlap(fund_id_1=funds[2].id, fund_id_2=funds[4].id, overlap_percentage=89.0, overlapping_stocks=4),
            FundOverlap(fund_id_1=funds[3].id, fund_id_2=funds[4].id, overlap_percentage=90.0, overlapping_stocks=4),
            FundOverlap(fund_id_1=funds[7].id, fund_id_2=funds[8].id, overlap_percentage=80.0, overlapping_stocks=3),
        ]
        db.add_all(overlaps)
        db.commit()

        # Generate historical NAV data
        today = datetime.now().date()
        for fund in funds:
            # Start from January 1, 2023
            start_date = datetime(2023, 1, 1).date()
            current_date = start_date

            # Set initial NAV value
            initial_nav = 100.0
            current_nav = initial_nav

            # Set growth trend and volatility parameters
            annual_growth_rate = 0.10 + random.uniform(-0.05, 0.05)  # 5-15% annual growth
            daily_volatility = 0.005  # 0.5% daily volatility

            # Generate daily NAV data
            while current_date <= today:
                # Calculate NAV with some randomness
                daily_change = random.normalvariate(annual_growth_rate / 365, daily_volatility)
                current_nav = max(current_nav * (1 + daily_change), current_nav * 0.95)  # Prevent large drops

                # Add NAV data point
                nav_record = HistoricalNAV(
                    fund_id=fund.id,
                    date=current_date,
                    nav=round(current_nav, 2)
                )
                db.add(nav_record)

                # Move to next day
                current_date += timedelta(days=1)

        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()