"""
Common test configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.main import app
from app.core.config import settings

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def mock_stock_data():
    """Mock data for stock tests"""
    return {
        "symbol": "VNM",
        "name": "Vietnam Dairy Products JSC",
        "exchange": "HOSE",
        "industry": "Consumer Goods",
        "market_cap": 168432000000,
        "volume": 1234567
    }

@pytest.fixture
def mock_stock_price_data():
    """Mock data for stock price tests"""
    today = datetime.now()
    return [
        {
            "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
            "open": 100000 + i * 100,
            "high": 101000 + i * 100,
            "low": 99000 + i * 100,
            "close": 100500 + i * 100,
            "volume": 1000000 + i * 1000
        }
        for i in range(30)
    ]

@pytest.fixture
def mock_stock_financial_data():
    """Mock data for stock financial tests"""
    return {
        "symbol": "VNM",
        "revenue": 60234000000,
        "profit": 11234000000,
        "assets": 123456000000,
        "equity": 98765000000,
        "eps": 4567,
        "pe": 15.6,
        "roe": 12.3
    }

@pytest.fixture
def api_headers():
    """Common API headers"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    } 