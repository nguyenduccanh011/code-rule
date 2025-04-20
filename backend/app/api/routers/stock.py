from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from app.services.stock_data import StockDataService
# from app.core.auth import get_current_user

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"]
    # dependencies=[Depends(get_current_user)]
)

@router.get("/list")
async def get_stock_list():
    """
    Lấy danh sách mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        stock_list = stock_service.get_stock_list()
        if stock_list is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve stock list")
        return stock_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/price")
async def get_stock_price(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    days: int = 30
):
    """
    Lấy dữ liệu giá cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
        start_date: Ngày bắt đầu (YYYY-MM-DD)
        end_date: Ngày kết thúc (YYYY-MM-DD)
        days: Số ngày dữ liệu cần lấy (nếu không chỉ định start_date và end_date)
    """
    try:
        # Xử lý ngày tháng
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
        # Kiểm tra ngày hợp lệ
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end < start:
            raise HTTPException(
                status_code=400,
                detail="end_date must be greater than or equal to start_date"
            )
            
        # Lấy dữ liệu
        stock_service = StockDataService()
        data = stock_service.get_stock_price(symbol, start_date, end_date)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/info")
async def get_stock_info(symbol: str):
    """
    Lấy thông tin cơ bản của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        info = stock_service.get_stock_info(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/basic-info")
async def get_stock_basic_info(symbol: str):
    """
    Lấy thông tin cơ bản chi tiết của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        info = stock_service.get_stock_basic_info(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/management")
async def get_stock_management(symbol: str):
    """
    Lấy thông tin ban lãnh đạo của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        info = stock_service.get_stock_management(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/major-shareholders")
async def get_stock_major_shareholders(symbol: str):
    """
    Lấy thông tin cổ đông lớn của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        info = stock_service.get_stock_major_shareholders(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/dividend-history")
async def get_stock_dividend_history(symbol: str):
    """
    Lấy lịch sử cổ tức của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        info = stock_service.get_stock_dividend_history(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/events")
async def get_stock_events(symbol: str):
    """
    Lấy thông tin sự kiện của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        info = stock_service.get_stock_events(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/financials")
async def get_stock_financials(
    symbol: str,
    report_type: str = 'balance_sheet',
    period: str = 'year',
    lang: str = 'vi'
):
    """
    Lấy báo cáo tài chính của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
        report_type: Loại báo cáo ('balance_sheet', 'income_statement', 'cash_flow')
        period: Kỳ báo cáo ('year', 'quarter')
        lang: Ngôn ngữ ('vi', 'en')
    """
    try:
        stock_service = StockDataService()
        data = stock_service.get_stock_financials(
            symbol=symbol,
            report_type=report_type,
            period=period,
            lang=lang
        )
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/screen")
async def screen_stocks(
    limit: int = 100
):
    """
    Lọc cổ phiếu theo tiêu chí
    
    Args:
        limit: Số lượng kết quả tối đa
    """
    try:
        stock_service = StockDataService()
        stocks = stock_service.screen_stocks(limit=limit)
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/technical-analysis")
async def get_technical_analysis(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    days: int = 30,
    indicators: List[str] = ["MA", "RSI", "MACD", "BB"]
):
    """
    Lấy phân tích kỹ thuật của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
        start_date: Ngày bắt đầu (YYYY-MM-DD)
        end_date: Ngày kết thúc (YYYY-MM-DD)
        days: Số ngày dữ liệu cần lấy (nếu không chỉ định start_date và end_date)
        indicators: Danh sách các chỉ báo kỹ thuật cần tính toán
    """
    try:
        # Xử lý ngày tháng
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
        # Kiểm tra ngày hợp lệ
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            if end < start:
                raise HTTPException(
                    status_code=400,
                    detail="end_date must be greater than or equal to start_date"
                )
                
            # Kiểm tra ngày không vượt quá hiện tại
            today = datetime.now()
            if start > today or end > today:
                raise HTTPException(
                    status_code=400,
                    detail="Dates cannot be in the future"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format. Please use YYYY-MM-DD format: {str(e)}"
            )
            
        # Lấy dữ liệu
        stock_service = StockDataService()
        data = stock_service.get_technical_analysis(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            indicators=indicators
        )
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str):
    """
    Lấy phân tích cơ bản của cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu
    """
    try:
        stock_service = StockDataService()
        analysis = stock_service.get_fundamental_analysis(symbol)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/analysis")
async def get_portfolio_analysis(
    symbols: List[str],
    weights: Optional[List[float]] = None
):
    """
    Phân tích danh mục đầu tư
    
    Args:
        symbols: Danh sách mã cổ phiếu trong danh mục
        weights: Tỷ trọng của từng cổ phiếu (nếu không có sẽ tính bằng nhau)
    """
    try:
        if weights and len(weights) != len(symbols):
            raise HTTPException(
                status_code=400,
                detail="Number of weights must match number of symbols"
            )
            
        stock_service = StockDataService()
        analysis = stock_service.get_portfolio_analysis(
            symbols=symbols,
            weights=weights
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/performance")
async def get_portfolio_performance(
    symbols: List[str],
    weights: Optional[List[float]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Theo dõi hiệu suất danh mục đầu tư
    
    Args:
        symbols: Danh sách mã cổ phiếu trong danh mục
        weights: Tỷ trọng của từng cổ phiếu (nếu không có sẽ tính bằng nhau)
        start_date: Ngày bắt đầu (YYYY-MM-DD)
        end_date: Ngày kết thúc (YYYY-MM-DD)
    """
    try:
        if weights and len(weights) != len(symbols):
            raise HTTPException(
                status_code=400,
                detail="Number of weights must match number of symbols"
            )
            
        # Xử lý ngày tháng
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
        stock_service = StockDataService()
        performance = stock_service.get_portfolio_performance(
            symbols=symbols,
            weights=weights,
            start_date=start_date,
            end_date=end_date
        )
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 