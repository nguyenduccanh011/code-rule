#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ví dụ về cách lấy thông tin công ty từ vnstock
"""

from vnstock import Vnstock
import pandas as pd

def company_info_example():
    """Ví dụ về cách lấy và phân tích thông tin công ty"""
    
    # 1. Khởi tạo đối tượng
    print("\n1. Khởi tạo đối tượng")
    stock = Vnstock().stock(symbol='VCI', source='VCI')
    
    # 2. Lấy thông tin tổng quan
    print("\n2. Lấy thông tin tổng quan")
    overview = stock.company.overview()
    print("\nThông tin tổng quan:")
    print(overview)
    
    # 3. Lấy thông tin cơ bản
    print("\n3. Lấy thông tin cơ bản")
    basic_info = stock.company.basic_info()
    print("\nThông tin cơ bản:")
    print(basic_info)
    
    # 4. Lấy thông tin ban lãnh đạo
    print("\n4. Lấy thông tin ban lãnh đạo")
    management = stock.company.management()
    print("\nBan lãnh đạo:")
    print(management)
    
    # 5. Lấy thông tin cổ đông lớn
    print("\n5. Lấy thông tin cổ đông lớn")
    major_shareholders = stock.company.major_shareholders()
    print("\nCổ đông lớn:")
    print(major_shareholders)
    
    # 6. Lấy thông tin lịch sử cổ tức
    print("\n6. Lấy thông tin lịch sử cổ tức")
    dividend_history = stock.company.dividend_history()
    print("\nLịch sử cổ tức:")
    print(dividend_history)
    
    # 7. Lấy thông tin sự kiện
    print("\n7. Lấy thông tin sự kiện")
    events = stock.company.events()
    print("\nSự kiện:")
    print(events)

if __name__ == "__main__":
    try:
        company_info_example()
        print("\nVí dụ hoàn thành thành công!")
    except Exception as e:
        print(f"\nLỗi trong quá trình chạy ví dụ: {str(e)}") 