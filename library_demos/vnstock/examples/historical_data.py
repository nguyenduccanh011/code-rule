#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ví dụ về cách lấy và phân tích dữ liệu lịch sử từ vnstock
"""

from vnstock import Vnstock
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def historical_data_example():
    """Ví dụ về cách lấy và phân tích dữ liệu lịch sử"""
    
    # 1. Khởi tạo đối tượng
    print("\n1. Khởi tạo đối tượng")
    stock = Vnstock().stock(symbol='VCI', source='VCI')
    
    # 2. Lấy dữ liệu theo ngày
    print("\n2. Lấy dữ liệu theo ngày")
    daily_data = stock.quote.history(
        start_date='2023-01-01',
        end_date='2024-03-25',
        resolution='1D'
    )
    print("\nDữ liệu theo ngày:")
    print(daily_data.head())
    
    # 3. Lấy dữ liệu theo tuần
    print("\n3. Lấy dữ liệu theo tuần")
    weekly_data = stock.quote.history(
        start_date='2023-01-01',
        end_date='2024-03-25',
        resolution='1W'
    )
    print("\nDữ liệu theo tuần:")
    print(weekly_data.head())
    
    # 4. Lấy dữ liệu theo tháng
    print("\n4. Lấy dữ liệu theo tháng")
    monthly_data = stock.quote.history(
        start_date='2020-01-01',
        end_date='2024-03-25',
        resolution='1M'
    )
    print("\nDữ liệu theo tháng:")
    print(monthly_data.head())
    
    # 5. Lấy dữ liệu trong ngày
    print("\n5. Lấy dữ liệu trong ngày")
    intraday_data = stock.quote.intraday(page_size=1000)
    print("\nDữ liệu trong ngày:")
    print(intraday_data.head())
    
    # 6. Phân tích dữ liệu
    print("\n6. Phân tích dữ liệu")
    
    # Tính toán các chỉ số
    daily_data['MA20'] = daily_data['close'].rolling(window=20).mean()
    daily_data['MA50'] = daily_data['close'].rolling(window=50).mean()
    daily_data['Volume_MA20'] = daily_data['volume'].rolling(window=20).mean()
    
    # Vẽ biểu đồ giá và khối lượng
    plt.figure(figsize=(15, 10))
    
    # Biểu đồ giá
    plt.subplot(2, 1, 1)
    plt.plot(daily_data.index, daily_data['close'], label='Giá đóng cửa')
    plt.plot(daily_data.index, daily_data['MA20'], label='MA20')
    plt.plot(daily_data.index, daily_data['MA50'], label='MA50')
    plt.title('Biểu đồ Giá và Đường trung bình')
    plt.legend()
    plt.grid(True)
    
    # Biểu đồ khối lượng
    plt.subplot(2, 1, 2)
    plt.bar(daily_data.index, daily_data['volume'], label='Khối lượng')
    plt.plot(daily_data.index, daily_data['Volume_MA20'], label='Khối lượng MA20', color='red')
    plt.title('Biểu đồ Khối lượng')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('historical_analysis.png')
    print("Đã lưu biểu đồ phân tích vào file historical_analysis.png")
    
    # 7. Thống kê cơ bản
    print("\n7. Thống kê cơ bản")
    stats = {
        'Giá cao nhất': daily_data['high'].max(),
        'Giá thấp nhất': daily_data['low'].min(),
        'Giá trung bình': daily_data['close'].mean(),
        'Độ lệch chuẩn': daily_data['close'].std(),
        'Khối lượng trung bình': daily_data['volume'].mean()
    }
    print("\nThống kê cơ bản:")
    for key, value in stats.items():
        print(f"{key}: {value:,.2f}")

if __name__ == "__main__":
    try:
        historical_data_example()
        print("\nVí dụ hoàn thành thành công!")
    except Exception as e:
        print(f"\nLỗi trong quá trình chạy ví dụ: {str(e)}") 