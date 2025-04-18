from typing import Dict, List, Optional
import vnstock
from datetime import datetime, timedelta
import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class StockDataService:
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get_stock_price(self, symbol: str, start_date: str, end_date: str) -> Dict:
        """
        Lấy dữ liệu giá cổ phiếu từ vnstock
        
        Args:
            symbol: Mã cổ phiếu (ví dụ: 'VIC')
            start_date: Ngày bắt đầu (format: 'YYYY-MM-DD')
            end_date: Ngày kết thúc (format: 'YYYY-MM-DD')
            
        Returns:
            Dict chứa dữ liệu giá cổ phiếu
        """
        try:
            # Kiểm tra cache trước
            cache_file = self.cache_dir / f"{symbol}_{start_date}_{end_date}.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Lấy dữ liệu từ vnstock
            data = vnstock.stock_historical_data(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date
            )
            
            # Lưu vào cache
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data.to_dict('records'), f, ensure_ascii=False)
                
            return data.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting stock price for {symbol}: {str(e)}")
            raise
            
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Lấy thông tin cơ bản của cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu
            
        Returns:
            Dict chứa thông tin cổ phiếu
        """
        try:
            return vnstock.stock_info(symbol)
        except Exception as e:
            logger.error(f"Error getting stock info for {symbol}: {str(e)}")
            raise
            
    def get_stock_list(self) -> List[str]:
        """
        Lấy danh sách mã cổ phiếu
        
        Returns:
            List các mã cổ phiếu
        """
        try:
            return vnstock.stock_listing()
        except Exception as e:
            logger.error(f"Error getting stock list: {str(e)}")
            raise 