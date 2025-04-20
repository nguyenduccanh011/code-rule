from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any
from .stock_data import StockDataService
from .cache import CacheManager
import pandas as pd

logger = logging.getLogger(__name__)

class DataJobs:
    def __init__(self):
        self.stock_service = StockDataService()
        self.cache_manager = CacheManager()
        
    def update_stock_prices(self, symbols: List[str], days: int = 30) -> None:
        """
        Cập nhật dữ liệu giá cổ phiếu cho danh sách mã
        
        Args:
            symbols: Danh sách mã cổ phiếu
            days: Số ngày dữ liệu cần cập nhật
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        for symbol in symbols:
            try:
                logger.info(f"Updating price data for {symbol}")
                data = self.stock_service.get_stock_price(symbol, start_date, end_date)
                # Convert DataFrame to dict for caching
                if isinstance(data, pd.DataFrame):
                    data_dict = data.to_dict('records')
                    self.cache_manager.set(f"price_{symbol}", data_dict)
                else:
                    self.cache_manager.set(f"price_{symbol}", data)
            except Exception as e:
                logger.error(f"Error updating price data for {symbol}: {str(e)}")
                
    def update_stock_list(self) -> None:
        """
        Cập nhật danh sách cổ phiếu
        """
        try:
            logger.info("Updating stock list")
            stock_list = self.stock_service.get_stock_list()
            self.cache_manager.set("stock_list", stock_list)
        except Exception as e:
            logger.error(f"Error updating stock list: {str(e)}")
            
    def update_stock_info(self, symbols: List[str]) -> None:
        """
        Cập nhật thông tin cơ bản của cổ phiếu
        
        Args:
            symbols: Danh sách mã cổ phiếu
        """
        for symbol in symbols:
            try:
                logger.info(f"Updating info for {symbol}")
                info = self.stock_service.get_stock_info(symbol)
                self.cache_manager.set(f"info_{symbol}", info)
            except Exception as e:
                logger.error(f"Error updating info for {symbol}: {str(e)}")
                
    def run_daily_jobs(self) -> None:
        """
        Chạy các job cập nhật dữ liệu hàng ngày
        """
        try:
            # Cập nhật danh sách cổ phiếu
            self.update_stock_list()
            
            # Lấy danh sách cổ phiếu từ cache
            stock_list = self.cache_manager.get("stock_list")
            if not stock_list:
                logger.error("Failed to get stock list")
                return
                
            # Extract symbols from stock list
            symbols = [item.get('symbol') for item in stock_list if item.get('symbol')]
            
            # Cập nhật giá và thông tin cho tất cả cổ phiếu
            self.update_stock_prices(symbols)
            self.update_stock_info(symbols)
            
        except Exception as e:
            logger.error(f"Error running daily jobs: {str(e)}")
            raise 