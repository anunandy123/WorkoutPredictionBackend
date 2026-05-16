"""
Validation functions for user inputs.
"""
from app.utils.constants import DIFFICULTY_LEVELS , MUSCLE_GROUPS , WORKOUT_DAYS , FITNESS_LEVELS , FITNESS_GOALS

def validate_age(age: int) -> bool:
    """Validate age is positive."""
    return age > 0

def validate_difficulty(diff: str) -> bool:
    """avlidates the difficulty level of any excesise"""
    return diff in DIFFICULTY_LEVELS

def validate_day_name(n: str) -> bool:
    """validates the day name"""
    return n in WORKOUT_DAYS

def validate_fitness_levels(f: str) -> bool:
    """validates resonalble fitness level"""
    return f in FITNESS_LEVELS

def validate_fitness_goals(f: str) -> bool:
    """validates resonalble fitness goals"""
    return f in FITNESS_GOALS

def validate_muscle_groups(m: str) -> bool:
    """validates resonalble muscle group"""
    return m in MUSCLE_GROUPS

def validate_height(height: float) -> bool:
    """Validate height is between 50cm and 300cm."""
    return 50 <= height <= 300


def validate_weight(weight: float) -> bool:
    """Validate weight is positive and reasonable."""
    return 20 < weight <= 200


def validate_stress_level(level: int) -> bool:
    """Validate stress level is between 1 and 10."""
    return 1 <= level <= 10


def validate_energy_level(level: int) -> bool:
    """Validate energy level is between 1 and 10."""
    return 1 <= level <= 10


def validate_workout_days(days: int) -> bool:
    """Validate workout days is between 0 and 7."""
    return 0 <= days <= 7


def validate_password(password: str) -> bool:
    """Validate password is at least 6 characters."""
    return len(password) >= 6
