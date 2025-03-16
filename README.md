

Tech Stack
Frontend

Framework: React.js with functional components and hooks
Routing: React Router v6
State Management: React Context API
API Client: Axios
Styling: TailwindCSS
Charts: Recharts
Icons: Lucide React

Backend

Framework: FastAPI
Database ORM: SQLAlchemy
Authentication: JWT with FastAPI Auth
Validation: Pydantic
Migration: Alembic

Database

Service: PostgreSQL with Supabase
Features: Row-level security, functions for complex calculations

Prerequisites

Node.js (v16+)
Python (v3.9+)
PostgreSQL or Supabase account
Git

Installation
Clone the repository
bashCopygit clone https://github.com/your-username/investment-dashboard.git
cd investment-dashboard
Frontend Setup
bashCopy# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Update .env with your backend URL
# REACT_APP_API_URL=http://localhost:8000/api

# Start development server
npm start
Backend Setup
bashCopy# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your database URL and other settings
# DATABASE_URL=postgresql://postgres:password@localhost:5432/investment_dashboard
# SECRET_KEY=your-secret-key

# Start FastAPI server
uvicorn app.main:app --reload
Database Setup with Supabase

Create a new project in Supabase
Get your connection string from the Supabase dashboard
Update the DATABASE_URL in your backend .env file
Run database migrations:
bashCopycd backend
alembic upgrade head

Alternatively, execute the SQL scripts in the supabase-setup.sql file in the Supabase SQL editor

Project Structure
The project follows a clean architecture approach with clear separation of concerns:
Copyinvestment-dashboard/
├── frontend/                # React frontend application
│   ├── public/              # Static assets
│   └── src/                 # Source code
│       ├── components/      # Reusable UI components
│       ├── pages/           # Page components
│       ├── services/        # API service layer
│       └── hooks/           # Custom React hooks
├── backend/                 # FastAPI backend application
│   ├── app/                 # Application code
│   │   ├── routers/         # API route handlers
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   └── alembic/             # Database migrations
└── docs/                    # Documentation
API Endpoints
GET - /api/users/{user_id} - Get user details
GET - /api/investments/dashboard/{user_id} - Get dashboard summary data
GET - /api/investments/user/{user_id} - Get user investments
GET - /api/analysis/sector-allocation/{user_id} - Get sector allocation
GET - /api/analysis/overlap/{user_id} - Get fund overlap analysis
GET/api/funds/{fund_id} - Get fund details
Deployment
Frontend Deployment (Vercel)

Connect your GitHub repository to Vercel
Configure environment variables
Deploy

Backend Deployment (Render)

Connect your GitHub repository to Render
Set up a web service with the following settings:

Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT


Configure environment variables
Deploy

Database (Supabase)

No additional deployment steps needed as Supabase is a managed service
