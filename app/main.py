from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.routers import users, investments, funds, analysis
from app.database import engine, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Investment Dashboard API",
    description="API for Investment Dashboard",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(investments.router, prefix="/api/investments", tags=["investments"])
app.include_router(funds.router, prefix="/api/funds", tags=["funds"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to Investment Dashboard API"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)