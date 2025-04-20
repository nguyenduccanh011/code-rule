from pathlib import Path
import json
from datetime import datetime, timedelta
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get(self, key: str, max_age_hours: int = 24) -> Optional[Dict]:
        """
        Lấy dữ liệu từ cache nếu còn hiệu lực
        
        Args:
            key: Key của cache
            max_age_hours: Thời gian tối đa cache được lưu (giờ)
            
        Returns:
            Dữ liệu từ cache hoặc None nếu không có hoặc hết hạn
        """
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Kiểm tra thời gian cache
            cache_time = datetime.fromisoformat(data.get('timestamp', ''))
            if datetime.now() - cache_time > timedelta(hours=max_age_hours):
                return None
                
            return data.get('data')
            
        except Exception as e:
            logger.error(f"Error reading cache for {key}: {str(e)}")
            return None
            
    def set(self, key: str, data: Any) -> None:
        """
        Lưu dữ liệu vào cache
        
        Args:
            key: Key của cache
            data: Dữ liệu cần lưu
        """
        try:
            cache_file = self.cache_dir / f"{key}.json"
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error writing cache for {key}: {str(e)}")
            raise
            
    def clear(self, key: Optional[str] = None) -> None:
        """
        Xóa cache
        
        Args:
            key: Key cần xóa, nếu None thì xóa toàn bộ cache
        """
        try:
            if key:
                cache_file = self.cache_dir / f"{key}.json"
                if cache_file.exists():
                    cache_file.unlink()
            else:
                for file in self.cache_dir.glob("*.json"):
                    file.unlink()
                    
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            raise 