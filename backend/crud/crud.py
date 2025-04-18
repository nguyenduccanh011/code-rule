from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from uuid import UUID

from models import models
from schemas import schemas
from core.security import get_password_hash, verify_password

# Base CRUD class
class CRUDBase:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: UUID) -> Optional[models.Base]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[models.Base]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: schemas.BaseSchema) -> models.Base:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: models.Base,
        obj_in: Union[schemas.BaseSchema, Dict[str, Any]]
    ) -> models.Base:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> models.Base:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

# User CRUD
class CRUDUser(CRUDBase):
    def __init__(self):
        super().__init__(models.User)

    def get_by_email(self, db: Session, *, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: models.User,
        obj_in: Union[schemas.UserUpdate, Dict[str, Any]]
    ) -> models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[models.User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: models.User) -> bool:
        return user.is_active

    def is_superuser(self, user: models.User) -> bool:
        return user.is_superuser

# Stock CRUD
class CRUDStock(CRUDBase):
    def __init__(self):
        super().__init__(models.Stock)

    def get_by_symbol(self, db: Session, *, symbol: str) -> Optional[models.Stock]:
        return db.query(models.Stock).filter(models.Stock.symbol == symbol).first()

    def get_multi_by_exchange(
        self, db: Session, *, exchange: str, skip: int = 0, limit: int = 100
    ) -> List[models.Stock]:
        return (
            db.query(models.Stock)
            .filter(models.Stock.exchange == exchange)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Price Data CRUD
class CRUDPriceData(CRUDBase):
    def __init__(self):
        super().__init__(models.PriceData)

    def get_by_stock_and_date(
        self, db: Session, *, stock_id: UUID, date: datetime
    ) -> Optional[models.PriceData]:
        return (
            db.query(models.PriceData)
            .filter(
                and_(
                    models.PriceData.stock_id == stock_id,
                    models.PriceData.date == date,
                )
            )
            .first()
        )

    def get_multi_by_stock(
        self,
        db: Session,
        *,
        stock_id: UUID,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.PriceData]:
        return (
            db.query(models.PriceData)
            .filter(
                and_(
                    models.PriceData.stock_id == stock_id,
                    models.PriceData.date >= start_date,
                    models.PriceData.date <= end_date,
                )
            )
            .order_by(models.PriceData.date)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Financial Data CRUD
class CRUDFinancialData(CRUDBase):
    def __init__(self):
        super().__init__(models.FinancialData)

    def get_by_stock_and_period(
        self,
        db: Session,
        *,
        stock_id: UUID,
        data_type: str,
        period: str
    ) -> Optional[models.FinancialData]:
        return (
            db.query(models.FinancialData)
            .filter(
                and_(
                    models.FinancialData.stock_id == stock_id,
                    models.FinancialData.data_type == data_type,
                    models.FinancialData.period == period,
                )
            )
            .first()
        )

# Strategy CRUD
class CRUDStrategy(CRUDBase):
    def __init__(self):
        super().__init__(models.Strategy)

    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Strategy]:
        return (
            db.query(models.Strategy)
            .filter(models.Strategy.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_public_strategies(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[models.Strategy]:
        return (
            db.query(models.Strategy)
            .filter(models.Strategy.is_public == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Backtest CRUD
class CRUDBacktest(CRUDBase):
    def __init__(self):
        super().__init__(models.Backtest)

    def get_multi_by_strategy(
        self,
        db: Session,
        *,
        strategy_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Backtest]:
        return (
            db.query(models.Backtest)
            .filter(models.Backtest.strategy_id == strategy_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Portfolio CRUD
class CRUDPortfolio(CRUDBase):
    def __init__(self):
        super().__init__(models.Portfolio)

    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Portfolio]:
        return (
            db.query(models.Portfolio)
            .filter(models.Portfolio.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Position CRUD
class CRUDPosition(CRUDBase):
    def __init__(self):
        super().__init__(models.Position)

    def get_multi_by_portfolio(
        self,
        db: Session,
        *,
        portfolio_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Position]:
        return (
            db.query(models.Position)
            .filter(models.Position.portfolio_id == portfolio_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Create instances
crud_user = CRUDUser()
crud_stock = CRUDStock()
crud_price_data = CRUDPriceData()
crud_financial_data = CRUDFinancialData()
crud_strategy = CRUDStrategy()
crud_backtest = CRUDBacktest()
crud_portfolio = CRUDPortfolio()
crud_position = CRUDPosition() 