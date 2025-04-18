from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..services import StockDataService, CacheManager
from ..core.auth import get_current_user

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/list")
async def get_stock_list():
    """
    Lấy danh sách mã cổ phiếu
    """
    try:
        cache_manager = CacheManager()
        stock_list = cache_manager.get("stock_list")
        
        if not stock_list:
            stock_service = StockDataService()
            stock_list = stock_service.get_stock_list()
            cache_manager.set("stock_list", stock_list)
            
        return {"data": stock_list}
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
            
        # Lấy dữ liệu
        stock_service = StockDataService()
        data = stock_service.get_stock_price(symbol, start_date, end_date)
        
        return {"data": data}
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
        cache_manager = CacheManager()
        cache_key = f"info_{symbol}"
        info = cache_manager.get(cache_key)
        
        if not info:
            stock_service = StockDataService()
            info = stock_service.get_stock_info(symbol)
            cache_manager.set(cache_key, info)
            
        return {"data": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 