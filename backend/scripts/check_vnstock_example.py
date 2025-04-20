from vnstock import Vnstock, Screener, Listing
import pandas as pd

def check_stock_data():
    """Kiểm tra các chức năng lấy dữ liệu cổ phiếu"""
    print("Trying to get stock data for VNM:")
    try:
        stock = Vnstock().stock(symbol='VNM', source='TCBS')
        
        # Lấy dữ liệu lịch sử
        print("\nHistorical data:")
        hist_data = stock.quote.history(
            start='2023-01-01',
            end='2023-12-31',
            interval='1D'
        )
        print(hist_data.head())
        
        # Lấy thông tin công ty
        print("\nCompany overview:")
        overview = stock.company.overview()
        print(overview)
        
        # Lấy báo cáo tài chính
        print("\nFinancial data:")
        fin_data = stock.financial.report(
            report_type="bs",
            report_range="year",
            language="vi"
        )
        print(fin_data.head())
        
        # Lấy chỉ số tài chính
        print("\nFinancial ratio:")
        ratio = stock.financial.ratio(report_range="year")
        print(ratio.head())
        
    except Exception as e:
        print(f"Error: {e}")

def check_screener():
    """Kiểm tra chức năng lọc cổ phiếu"""
    print("\nTrying to use screener:")
    try:
        screener = Screener(source='TCBS')
        
        # Lọc cổ phiếu theo sàn
        stocks = screener.stock(
            params={"exchangeName": "HOSE,HNX"},
            limit=5
        )
        print("Sample stocks:", stocks)
        
        # Phân tích kỹ thuật
        technical = screener.technical(
            symbol="VNM",
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
        print("\nTechnical analysis:", technical)
        
    except Exception as e:
        print(f"Error: {e}")

def check_listing():
    """Kiểm tra chức năng danh sách mã"""
    print("\nTrying to get stock listings:")
    try:
        listing = Listing()
        
        # Lấy danh sách mã
        symbols = listing.all_symbols()
        print(f"Found {len(symbols)} symbols")
        print("Sample symbols:", symbols[:5])
        
        # Lấy thông tin sàn
        exchanges = listing.exchanges()
        print("\nExchange information:", exchanges)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_stock_data()
    check_screener()
    check_listing() 