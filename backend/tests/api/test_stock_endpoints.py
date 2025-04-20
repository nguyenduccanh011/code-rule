"""
Tests for stock-related API endpoints
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

def test_get_stock_list(client, mock_stock_data):
    """Test lấy danh sách cổ phiếu"""
    with patch('app.services.stock_data.StockDataService.get_stock_list') as mock_get:
        mock_get.return_value = [mock_stock_data]
        response = client.get("/api/v1/stocks/list")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["symbol"] == mock_stock_data["symbol"]
        assert data[0]["name"] == mock_stock_data["name"]

def test_get_stock_price(client, mock_stock_price_data):
    """Test lấy dữ liệu giá cổ phiếu"""
    symbol = "VNM"
    with patch('app.services.stock_data.StockDataService.get_stock_price') as mock_get:
        mock_get.return_value = {"symbol": symbol, "data": mock_stock_price_data}
        response = client.get(f"/api/v1/stocks/{symbol}/price?days=30")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["symbol"] == symbol
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 30
        
        price_data = data["data"][0]
        assert "date" in price_data
        assert "close" in price_data
        assert "volume" in price_data

def test_get_stock_info(client, mock_stock_data):
    """Test lấy thông tin công ty"""
    symbol = "VNM"
    with patch('app.services.stock_data.StockDataService.get_stock_info') as mock_get:
        mock_get.return_value = mock_stock_data
        response = client.get(f"/api/v1/stocks/{symbol}/info")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["symbol"] == symbol
        assert data["name"] == mock_stock_data["name"]

def test_get_stock_financial_info(client, mock_stock_financial_data):
    """Test lấy thông tin tài chính"""
    symbol = "VNM"
    with patch('app.services.stock_data.StockDataService.get_stock_financials') as mock_get:
        mock_get.return_value = mock_stock_financial_data
        response = client.get(
            f"/api/v1/stocks/{symbol}/financials",
            params={"report_type": "balance_sheet", "period": "year"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["symbol"] == symbol
        assert "revenue" in data
        assert "profit" in data

def test_invalid_stock_symbol(client):
    """Test với mã cổ phiếu không hợp lệ"""
    symbol = "INVALID"
    with patch('app.services.stock_data.StockDataService.get_stock_price') as mock_get:
        mock_get.side_effect = Exception("Stock not found")
        response = client.get(f"/api/v1/stocks/{symbol}/price")
        assert response.status_code == 500

def test_invalid_date_format(client):
    """Test với định dạng ngày không hợp lệ"""
    symbol = "VNM"
    response = client.get(
        f"/api/v1/stocks/{symbol}/price",
        params={"start_date": "invalid-date"}
    )
    assert response.status_code == 400

def test_future_date(client):
    """Test với ngày trong tương lai"""
    symbol = "VNM"
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.get(
        f"/api/v1/stocks/{symbol}/price",
        params={"end_date": future_date}
    )
    assert response.status_code == 400

def test_end_date_before_start_date(client):
    """Test với ngày kết thúc trước ngày bắt đầu"""
    symbol = "VNM"
    end_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    start_date = datetime.now().strftime("%Y-%m-%d")
    response = client.get(
        f"/api/v1/stocks/{symbol}/price",
        params={"start_date": start_date, "end_date": end_date}
    )
    assert response.status_code == 400 