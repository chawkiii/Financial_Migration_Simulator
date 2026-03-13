# financial_simulator/database/models.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class Simulation(Base):

    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    initial_savings = Column(Integer)
    one_time_cost = Column(Integer)

    monthly_income = Column(Integer)
    monthly_expenses = Column(Integer)

    months = Column(Integer)
    savings_goal = Column(Integer)

    months_without_income = Column(Integer)


class SimulationResult(Base):

    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True)

    simulation_id = Column(Integer)

    final_balance = Column(Integer)

    financial_score = Column(Integer)

    success_probability = Column(Integer)

    risk_score = Column(Integer)

    risk_level = Column(String)