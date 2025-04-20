from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    strategies = relationship("Strategy", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(String(36), primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(255))
    exchange = Column(String(50))
    sector = Column(String(100))
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    price_data = relationship("PriceData", back_populates="stock")
    financial_data = relationship("FinancialData", back_populates="stock")

class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(String(36), primary_key=True)
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stock = relationship("Stock", back_populates="price_data")

class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(String(36), primary_key=True)
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    data_type = Column(String(50), nullable=False)  # income, balance, cashflow
    period = Column(String(20))  # Q1, Q2, Q3, Q4, Annual
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stock = relationship("Stock", back_populates="financial_data")

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    code = Column(Text, nullable=False)
    parameters = Column(JSON)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="strategies")
    backtests = relationship("Backtest", back_populates="strategy")

class Backtest(Base):
    __tablename__ = "backtests"

    id = Column(String(36), primary_key=True)
    strategy_id = Column(String(36), ForeignKey("strategies.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    parameters = Column(JSON)
    results = Column(JSON)
    status = Column(String(20))  # running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    strategy = relationship("Strategy", back_populates="backtests")

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    initial_capital = Column(Float, nullable=False)
    current_value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")

class Position(Base):
    __tablename__ = "positions"

    id = Column(String(36), primary_key=True)
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False)
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    average_price = Column(Float, nullable=False)
    current_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    stock = relationship("Stock") 