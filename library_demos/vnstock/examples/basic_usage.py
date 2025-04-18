#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ví dụ về cách sử dụng cơ bản của vnstock
"""

from vnstock import Vnstock, Screener, Listing
import pandas as pd

def basic_usage_example():
    """Ví dụ về cách sử dụng cơ bản"""
    
    # 1. Khởi tạo đối tượng Vnstock
    print("\n1. Khởi tạo đối tượng Vnstock")
    stock = Vnstock().stock(symbol='VCI', source='VCI')
    print(f"Đã khởi tạo đối tượng cho mã cổ phiếu: VCI")
    
    # 2. Lấy dữ liệu giá cơ bản
    print("\n2. Lấy dữ liệu giá cơ bản")
    quote = stock.quote.history(
        start_date='2024-01-01',
        end_date='2024-03-25',
        resolution='1D'
    )
    print("\nDữ liệu giá:")
    print(quote.head())
    
    # 3. Lấy thông tin công ty cơ bản
    print("\n3. Lấy thông tin công ty cơ bản")
    overview = stock.company.overview()
    print("\nThông tin tổng quan:")
    print(overview)
    
    # 4. Lấy dữ liệu tài chính cơ bản
    print("\n4. Lấy dữ liệu tài chính cơ bản")
    ratios = stock.finance.ratio(period='quarter', lang='en', is_all=True)
    print("\nCác chỉ số tài chính:")
    print(ratios.head())
    
    # 5. Sử dụng Screener cơ bản
    print("\n5. Sử dụng Screener cơ bản")
    screener = Screener(source='TCBS')
    filters = {
        "exchangeName": "HOSE,HNX",
        "marketCap": (1000, 10000)  # Tỷ VND
    }
    screened_stocks = screener.stock_screening_insights(params=filters, size=10)
    print("\nKết quả lọc cổ phiếu:")
    print(screened_stocks)
    
    # 6. Lấy danh sách mã cổ phiếu
    print("\n6. Lấy danh sách mã cổ phiếu")
    listing = Listing()
    symbols = listing.all_symbols()
    print("\nDanh sách mã cổ phiếu:")
    print(symbols.head())

if __name__ == "__main__":
    try:
        basic_usage_example()
        print("\nVí dụ hoàn thành thành công!")
    except Exception as e:
        print(f"\nLỗi trong quá trình chạy ví dụ: {str(e)}") 