import vnstock
from vnstock import Vnstock, Screener, Listing
import inspect

def check_vnstock_functions():
    """Kiểm tra các hàm có sẵn trong vnstock"""
    print("Functions in vnstock:")
    for name, obj in inspect.getmembers(vnstock):
        if inspect.isfunction(obj):
            print(f"- {name}")

def check_stock_list():
    """Kiểm tra lấy danh sách mã chứng khoán"""
    print("\nTrying to get stock list:")
    try:
        listing = Listing()
        symbols = listing.all_symbols()
        print(f"Found {len(symbols)} symbols")
        print("Sample symbols:", symbols[:5])
    except Exception as e:
        print(f"Error getting stock list: {e}")

def check_stock_data():
    """Kiểm tra lấy dữ liệu cổ phiếu"""
    print("\nTrying to get stock data for VNM:")
    try:
        stock = Vnstock().stock(symbol='VNM', source='TCBS')
        
        # Lấy dữ liệu lịch sử
        print("\nHistorical data:")
        history = stock.quote.history(
            start='2024-01-01',
            end='2024-03-19',
            interval='1D'
        )
        print(history.head())
        
        # Lấy thông tin công ty
        print("\nCompany overview:")
        overview = stock.company.overview()
        print(overview)
        
    except Exception as e:
        print(f"Error getting stock data: {e}")

def check_screener():
    """Kiểm tra chức năng lọc cổ phiếu"""
    print("\nTrying to use screener:")
    try:
        screener = Screener(source='TCBS')
        stocks = screener.stock(
            params={"exchangeName": "HOSE,HNX"},
            limit=5
        )
        print("Sample stocks:", stocks)
    except Exception as e:
        print(f"Error using screener: {e}")

if __name__ == "__main__":
    check_vnstock_functions()
    check_stock_list()
    check_stock_data()
    check_screener() 