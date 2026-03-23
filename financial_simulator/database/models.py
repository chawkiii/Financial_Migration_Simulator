# financial_simulator/database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    simulations = relationship("Simulation", back_populates="user")


class Simulation(Base):

    __tablename__ = "simulations"

    __table_args__ = (
        UniqueConstraint('user_id', 'inputs_hash', name='unique_user_simulation'),
    )

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    inputs_hash = Column(String, index=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    province = Column(String)

    inputs = Column(JSON)
    results = Column(JSON)

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
        uselist=False,
        cascade="all, delete-orphan"
    )


class SimulationResult(Base):

    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True)

    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False, unique=True)

    final_balance = Column(Float)
    financial_score = Column(Float)
    success_probability = Column(Float)

    risk_score = Column(Float)
    risk_level = Column(String)

    simulation = relationship("Simulation", back_populates="result")