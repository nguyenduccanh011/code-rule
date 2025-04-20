"""
Tests for StockDataService
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.services.stock_data import StockDataService

@pytest.fixture
def stock_service():
    """Stock service fixture"""
    return StockDataService()

def test_get_stock_list(stock_service, mock_stock_data):
    """Test lấy danh sách cổ phiếu"""
    with patch('vnstock.Listing.all_symbols') as mock_get:
        mock_get.return_value = [mock_stock_data]
        result = stock_service.get_stock_list()
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["symbol"] == mock_stock_data["symbol"]
        assert result[0]["name"] == mock_stock_data["name"]

def test_get_stock_price(stock_service, mock_stock_price_data):
    """Test lấy dữ liệu giá cổ phiếu"""
    symbol = "VNM"
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    mock_stock = MagicMock()
    mock_stock.quote.history.return_value = mock_stock_price_data
    
    with patch('vnstock.Vnstock.stock') as mock_stock_init:
        mock_stock_init.return_value = mock_stock
        result = stock_service.get_stock_price(symbol, start_date, end_date)
        
        assert isinstance(result, dict)
        assert result["symbol"] == symbol
        assert isinstance(result["data"], list)
        assert len(result["data"]) == len(mock_stock_price_data)

def test_get_stock_info(stock_service, mock_stock_data):
    """Test lấy thông tin công ty"""
    symbol = "VNM"
    with patch('vnstock.Vnstock.company_overview') as mock_get:
        mock_get.return_value = mock_stock_data
        result = stock_service.get_stock_info(symbol)
        
        assert isinstance(result, dict)
        assert result["symbol"] == symbol
        assert result["name"] == mock_stock_data["name"]

def test_get_stock_financials(stock_service, mock_stock_financial_data):
    """Test lấy thông tin tài chính"""
    symbol = "VNM"
    with patch('vnstock.Vnstock.financial_report') as mock_get:
        mock_get.return_value = mock_stock_financial_data
        result = stock_service.get_stock_financials(
            symbol,
            report_type="balance_sheet",
            period="year"
        )
        
        assert isinstance(result, dict)
        assert result["symbol"] == symbol
        assert "revenue" in result
        assert "profit" in result

def test_get_stock_list_empty(stock_service):
    """Test lấy danh sách cổ phiếu khi không có dữ liệu"""
    with patch('vnstock.Listing.all_symbols') as mock_get:
        mock_get.return_value = None
        result = stock_service.get_stock_list()
        assert isinstance(result, list)
        assert len(result) == 0

def test_get_stock_price_error(stock_service):
    """Test lấy giá cổ phiếu khi có lỗi"""
    symbol = "VNM"
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    with patch('vnstock.Vnstock.stock') as mock_stock:
        mock_stock.side_effect = Exception("API Error")
        with pytest.raises(Exception):
            stock_service.get_stock_price(symbol, start_date, end_date)

def test_cache_stock_list(stock_service, mock_stock_data):
    """Test cache danh sách cổ phiếu"""
    with patch('vnstock.Listing.all_symbols') as mock_get:
        mock_get.return_value = [mock_stock_data]
        
        # First call
        result1 = stock_service.get_stock_list()
        # Second call should use cache
        result2 = stock_service.get_stock_list()
        
        assert mock_get.call_count == 1  # Should only call API once
        assert result1 == result2 