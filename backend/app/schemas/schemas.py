from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID, uuid4

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class Token(BaseSchema):
    access_token: str
    token_type: str
    refresh_token: str

class TokenPayload(BaseSchema):
    sub: UUID
    exp: datetime

# Stock schemas
class StockBase(BaseSchema):
    symbol: str
    name: Optional[str] = None
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    pass

class Stock(StockBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Price Data schemas
class PriceDataBase(BaseSchema):
    stock_id: UUID
    date: datetime
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None

class PriceDataCreate(PriceDataBase):
    pass

class PriceDataUpdate(PriceDataBase):
    pass

class PriceData(PriceDataBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Financial Data schemas
class FinancialDataBase(BaseSchema):
    stock_id: UUID
    date: datetime
    data_type: str
    period: Optional[str] = None
    data: Dict[str, Any]

class FinancialDataCreate(FinancialDataBase):
    pass

class FinancialDataUpdate(FinancialDataBase):
    pass

class FinancialData(FinancialDataBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Strategy schemas
class StrategyBase(BaseSchema):
    name: str
    description: Optional[str] = None
    code: str
    parameters: Optional[Dict[str, Any]] = None
    is_public: bool = False

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

# Backtest schemas
class BacktestBase(BaseSchema):
    strategy_id: UUID
    start_date: datetime
    end_date: datetime
    initial_capital: float
    parameters: Optional[Dict[str, Any]] = None

class BacktestCreate(BacktestBase):
    pass

class BacktestUpdate(BacktestBase):
    status: Optional[str] = None
    results: Optional[Dict[str, Any]] = None

class Backtest(BacktestBase):
    id: UUID
    status: str
    results: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

# Portfolio schemas
class PortfolioBase(BaseSchema):
    name: str
    description: Optional[str] = None
    initial_capital: float

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(PortfolioBase):
    current_value: Optional[float] = None

class Portfolio(PortfolioBase):
    id: UUID
    user_id: UUID
    current_value: Optional[float] = None
    created_at: datetime
    updated_at: datetime

# Position schemas
class PositionBase(BaseSchema):
    portfolio_id: UUID
    stock_id: UUID
    quantity: int
    average_price: float

class PositionCreate(PositionBase):
    pass

class PositionUpdate(PositionBase):
    current_price: Optional[float] = None

class Position(PositionBase):
    id: UUID
    current_price: Optional[float] = None
    created_at: datetime
    updated_at: datetime

# Response schemas
class Message(BaseSchema):
    message: str

class HealthCheck(BaseSchema):
    status: str
    version: str
    database_status: str
    cache_status: str 