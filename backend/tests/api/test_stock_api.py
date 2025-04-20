import pytest
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_get_stock_list():
    """Test API lấy danh sách cổ phiếu"""
    response = requests.get(f"{BASE_URL}/stocks/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "symbol" in data[0]
        assert "name" in data[0]

def test_get_stock_price():
    """Test API lấy dữ liệu giá cổ phiếu"""
    symbol = "VNM"
    days = 30
    response = requests.get(f"{BASE_URL}/stocks/{symbol}/price?days={days}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "date" in data[0]
        assert "close" in data[0]
        assert "volume" in data[0]

def test_get_stock_info():
    """Test API lấy thông tin công ty"""
    symbol = "VNM"
    response = requests.get(f"{BASE_URL}/stocks/{symbol}/info")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "symbol" in data
    assert "name" in data

def test_invalid_stock_symbol():
    """Test API với mã cổ phiếu không hợp lệ"""
    symbol = "INVALID"
    response = requests.get(f"{BASE_URL}/stocks/{symbol}/price")
    assert response.status_code == 500

if __name__ == "__main__":
    pytest.main([__file__]) 