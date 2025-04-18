#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ví dụ về cách lấy và phân tích dữ liệu tài chính từ vnstock
"""

from vnstock import Vnstock
import pandas as pd
import matplotlib.pyplot as plt

def financial_data_example():
    """Ví dụ về cách lấy và phân tích dữ liệu tài chính"""
    
    # 1. Khởi tạo đối tượng
    print("\n1. Khởi tạo đối tượng")
    stock = Vnstock().stock(symbol='VCI', source='VCI')
    
    # 2. Lấy bảng cân đối kế toán
    print("\n2. Lấy bảng cân đối kế toán")
    balance_sheet = stock.finance.balance_sheet(period='year', lang='vi')
    print("\nBảng cân đối kế toán:")
    print(balance_sheet.head())
    
    # 3. Lấy báo cáo kết quả kinh doanh
    print("\n3. Lấy báo cáo kết quả kinh doanh")
    income_statement = stock.finance.income_statement(period='year', lang='vi')
    print("\nBáo cáo kết quả kinh doanh:")
    print(income_statement.head())
    
    # 4. Lấy báo cáo lưu chuyển tiền tệ
    print("\n4. Lấy báo cáo lưu chuyển tiền tệ")
    cash_flow = stock.finance.cash_flow(period='year', lang='vi')
    print("\nBáo cáo lưu chuyển tiền tệ:")
    print(cash_flow.head())
    
    # 5. Lấy các chỉ số tài chính
    print("\n5. Lấy các chỉ số tài chính")
    ratios = stock.finance.ratio(period='quarter', lang='en', is_all=True)
    print("\nCác chỉ số tài chính:")
    print(ratios.head())
    
    # 6. Phân tích xu hướng doanh thu
    print("\n6. Phân tích xu hướng doanh thu")
    revenue = income_statement[['revenue']]
    plt.figure(figsize=(12, 6))
    plt.plot(revenue.index, revenue['revenue'], marker='o')
    plt.title('Xu hướng Doanh thu')
    plt.xlabel('Năm')
    plt.ylabel('Doanh thu (tỷ VND)')
    plt.grid(True)
    plt.savefig('revenue_trend.png')
    print("Đã lưu biểu đồ xu hướng doanh thu vào file revenue_trend.png")
    
    # 7. Phân tích các chỉ số tài chính chính
    print("\n7. Phân tích các chỉ số tài chính chính")
    key_ratios = ratios[['roe', 'roa', 'eps']]
    print("\nCác chỉ số tài chính chính:")
    print(key_ratios.tail())
    
    # 8. Vẽ biểu đồ các chỉ số tài chính
    plt.figure(figsize=(12, 6))
    for column in key_ratios.columns:
        plt.plot(key_ratios.index, key_ratios[column], marker='o', label=column)
    plt.title('Các chỉ số tài chính chính')
    plt.xlabel('Quý')
    plt.ylabel('Giá trị')
    plt.legend()
    plt.grid(True)
    plt.savefig('key_ratios.png')
    print("Đã lưu biểu đồ các chỉ số tài chính vào file key_ratios.png")

if __name__ == "__main__":
    try:
        financial_data_example()
        print("\nVí dụ hoàn thành thành công!")
    except Exception as e:
        print(f"\nLỗi trong quá trình chạy ví dụ: {str(e)}") 