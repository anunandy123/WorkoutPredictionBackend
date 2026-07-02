from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import Base, engine
from app.routes import (
    equipment_routes,
    exercise_routes,
    food_routes,
    goal_routes,
    lifestyle_routes,
    prediction_routes,
    progress_routes,
    user_routes,
    workout_routes,
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Workout Prediction API",
    description="API for workout prediction and fitness tracking",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router)
app.include_router(goal_routes.router)
app.include_router(workout_routes.router)
app.include_router(exercise_routes.router)
app.include_router(equipment_routes.router)
app.include_router(food_routes.router)
app.include_router(lifestyle_routes.router)
app.include_router(progress_routes.router)
app.include_router(prediction_routes.router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to Workout Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}