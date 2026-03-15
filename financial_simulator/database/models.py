# financial_simulator/database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    simulations = relationship("Simulation", back_populates="user")


class Simulation(Base):

    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    province = Column(String)

    # Raw input/output JSON
    inputs = Column(JSON)
    results = Column(JSON)

    # Normalized inputs (useful for analytics)
    initial_savings = Column(Float)
    one_time_cost = Column(Float)
    monthly_income = Column(Float)
    monthly_expenses = Column(Float)
    months = Column(Integer)
    savings_goal = Column(Float)
    months_without_income = Column(Integer)
    tax_rate = Column(Float)

    user = relationship("User", back_populates="simulations")

    result = relationship(
        "SimulationResult",
        back_populates="simulation",
        uselist=False
    )


class SimulationResult(Base):

    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True)

    simulation_id = Column(Integer, ForeignKey("simulations.id"))

    final_balance = Column(Float)
    financial_score = Column(Float)
    success_probability = Column(Float)

    risk_score = Column(Float)
    risk_level = Column(String)

    simulation = relationship("Simulation", back_populates="result")