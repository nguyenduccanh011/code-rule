import logging
import schedule
import time
from datetime import datetime
from ..services import DataJobs

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_update_jobs():
    """
    Chạy các job cập nhật dữ liệu
    """
    try:
        logger.info("Starting data update jobs")
        data_jobs = DataJobs()
        data_jobs.run_daily_jobs()
        logger.info("Data update jobs completed successfully")
    except Exception as e:
        logger.error(f"Error running update jobs: {str(e)}")

def main():
    """
    Chạy script cập nhật dữ liệu
    """
    # Chạy job ngay lập tức
    run_update_jobs()
    
    # Lên lịch chạy hàng ngày vào 18:00
    schedule.every().day.at("18:00").do(run_update_jobs)
    
    logger.info("Data update service started")
    logger.info("Next update scheduled at 18:00")
    
    # Vòng lặp chính
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 