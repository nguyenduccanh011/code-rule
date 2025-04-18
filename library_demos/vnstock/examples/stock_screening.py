#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ví dụ về cách sử dụng bộ lọc cổ phiếu từ vnstock
"""

from vnstock import Screener
import pandas as pd
import matplotlib.pyplot as plt

def stock_screening_example():
    """Ví dụ về cách sử dụng bộ lọc cổ phiếu"""
    
    # 1. Khởi tạo bộ lọc
    print("\n1. Khởi tạo bộ lọc")
    screener = Screener(source='TCBS')
    
    # 2. Lọc cổ phiếu theo vốn hóa và P/E
    print("\n2. Lọc cổ phiếu theo vốn hóa và P/E")
    filters_vncap_pe = {
        "exchangeName": "HOSE,HNX",
        "marketCap": (1000, 10000),  # Tỷ VND
        "pe": (0, 15)
    }
    stocks_vncap_pe = screener.stock_screening_insights(params=filters_vncap_pe, size=100)
    print("\nCổ phiếu theo vốn hóa và P/E:")
    print(stocks_vncap_pe.head())
    
    # 3. Lọc cổ phiếu theo ROE và cổ tức
    print("\n3. Lọc cổ phiếu theo ROE và cổ tức")
    filters_roe_div = {
        "exchangeName": "HOSE,HNX",
        "roe": (15, 100),  # Phần trăm
        "dividendYield": (5, 20)  # Phần trăm
    }
    stocks_roe_div = screener.stock_screening_insights(params=filters_roe_div, size=100)
    print("\nCổ phiếu theo ROE và cổ tức:")
    print(stocks_roe_div.head())
    
    # 4. Lọc cổ phiếu theo tăng trưởng doanh thu
    print("\n4. Lọc cổ phiếu theo tăng trưởng doanh thu")
    filters_revenue = {
        "exchangeName": "HOSE,HNX",
        "revenueGrowth": (20, 100)  # Phần trăm
    }
    stocks_revenue = screener.stock_screening_insights(params=filters_revenue, size=100)
    print("\nCổ phiếu theo tăng trưởng doanh thu:")
    print(stocks_revenue.head())
    
    # 5. Phân tích phân phối P/E
    print("\n5. Phân tích phân phối P/E")
    if not stocks_vncap_pe.empty:
        plt.figure(figsize=(10, 6))
        plt.hist(stocks_vncap_pe['pe'], bins=20, edgecolor='black')
        plt.title('Phân phối P/E của cổ phiếu')
        plt.xlabel('P/E')
        plt.ylabel('Số lượng cổ phiếu')
        plt.grid(True)
        plt.savefig('pe_distribution.png')
        print("Đã lưu biểu đồ phân phối P/E vào file pe_distribution.png")
    
    # 6. Phân tích tương quan ROE và cổ tức
    print("\n6. Phân tích tương quan ROE và cổ tức")
    if not stocks_roe_div.empty:
        plt.figure(figsize=(10, 6))
        plt.scatter(stocks_roe_div['roe'], stocks_roe_div['dividendYield'])
        plt.title('Tương quan giữa ROE và Tỷ suất cổ tức')
        plt.xlabel('ROE (%)')
        plt.ylabel('Tỷ suất cổ tức (%)')
        plt.grid(True)
        plt.savefig('roe_dividend_correlation.png')
        print("Đã lưu biểu đồ tương quan vào file roe_dividend_correlation.png")
    
    # 7. Kết hợp nhiều tiêu chí
    print("\n7. Kết hợp nhiều tiêu chí")
    filters_combined = {
        "exchangeName": "HOSE,HNX",
        "marketCap": (1000, 10000),
        "pe": (0, 15),
        "roe": (15, 100),
        "dividendYield": (5, 20),
        "revenueGrowth": (20, 100)
    }
    stocks_combined = screener.stock_screening_insights(params=filters_combined, size=100)
    print("\nCổ phiếu theo tiêu chí kết hợp:")
    print(stocks_combined.head())

if __name__ == "__main__":
    try:
        stock_screening_example()
        print("\nVí dụ hoàn thành thành công!")
    except Exception as e:
        print(f"\nLỗi trong quá trình chạy ví dụ: {str(e)}") 