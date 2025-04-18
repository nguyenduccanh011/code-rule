#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ví dụ về các tính năng nâng cao của vnstock
"""

from vnstock import Vnstock, Screener
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def advanced_features_example():
    """Ví dụ về các tính năng nâng cao"""
    
    try:
        # 1. Phân tích kỹ thuật
        print("\n1. Phân tích kỹ thuật")
        stock = Vnstock().stock(symbol='VCI', source='VCI')
        
        # Lấy dữ liệu giá
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        data = stock.quote.history(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            resolution='1D'
        )
        
        if data.empty:
            print("Không có dữ liệu giá để phân tích")
            return
        
        # Tính các chỉ báo kỹ thuật
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA50'] = data['close'].rolling(window=50).mean()
        data['RSI'] = calculate_rsi(data['close'])
        
        # Vẽ biểu đồ
        plt.figure(figsize=(15, 10))
        
        # Biểu đồ giá và MA
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data['close'], label='Giá đóng cửa')
        plt.plot(data.index, data['MA20'], label='MA20')
        plt.plot(data.index, data['MA50'], label='MA50')
        plt.title('Biểu đồ Giá và Đường trung bình')
        plt.legend()
        plt.grid(True)
        
        # Biểu đồ RSI
        plt.subplot(2, 1, 2)
        plt.plot(data.index, data['RSI'], label='RSI')
        plt.axhline(y=70, color='r', linestyle='--')
        plt.axhline(y=30, color='g', linestyle='--')
        plt.title('Chỉ báo RSI')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('technical_analysis.png')
        print("Đã lưu biểu đồ phân tích kỹ thuật vào file technical_analysis.png")
        
        # 2. Phân tích cơ bản nâng cao
        print("\n2. Phân tích cơ bản nâng cao")
        
        # Lấy dữ liệu tài chính
        ratios = stock.finance.ratio(period='quarter', lang='en', is_all=True)
        income = stock.finance.income_statement(period='year', lang='vi')
        
        if ratios.empty or income.empty:
            print("Không có dữ liệu tài chính để phân tích")
            return
        
        # Tính toán các chỉ số
        growth_metrics = calculate_growth_metrics(income)
        profitability_metrics = calculate_profitability_metrics(ratios)
        
        print("\nChỉ số tăng trưởng:")
        print(growth_metrics)
        print("\nChỉ số sinh lời:")
        print(profitability_metrics)
        
        # 3. Phân tích ngành
        print("\n3. Phân tích ngành")
        screener = Screener(source='TCBS')
        
        # Lọc cổ phiếu cùng ngành
        industry_filters = {
            "exchangeName": "HOSE,HNX",
            "industry": "Ngân hàng"  # Thay đổi theo ngành cần phân tích
        }
        industry_stocks = screener.stock_screening_insights(params=industry_filters, size=100)
        
        if industry_stocks.empty:
            print("Không có dữ liệu ngành để phân tích")
            return
        
        # Tính toán các chỉ số trung bình ngành
        industry_metrics = calculate_industry_metrics(industry_stocks)
        print("\nChỉ số trung bình ngành:")
        print(industry_metrics)
        
        # 4. Phân tích rủi ro
        print("\n4. Phân tích rủi ro")
        risk_metrics = calculate_risk_metrics(data)
        print("\nChỉ số rủi ro:")
        print(risk_metrics)
        
        # 5. Dự báo giá
        print("\n5. Dự báo giá")
        forecast = simple_price_forecast(data)
        print("\nDự báo giá trong 5 ngày tới:")
        print(forecast)
        
    except Exception as e:
        print(f"Lỗi trong quá trình phân tích: {str(e)}")

def calculate_rsi(prices, period=14):
    """Tính chỉ báo RSI"""
    if len(prices) < period:
        return pd.Series([np.nan] * len(prices), index=prices.index)
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Xử lý trường hợp loss = 0
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.fillna(50)  # Thay thế NaN bằng 50 (trung bình)

def calculate_growth_metrics(income_data):
    """Tính các chỉ số tăng trưởng"""
    if income_data.empty:
        return pd.DataFrame()
    
    metrics = {}
    try:
        metrics['revenue_growth'] = income_data['revenue'].pct_change() * 100
        metrics['profit_growth'] = income_data['net_income'].pct_change() * 100
    except KeyError as e:
        print(f"Không tìm thấy cột dữ liệu: {str(e)}")
        return pd.DataFrame()
    
    return pd.DataFrame(metrics)

def calculate_profitability_metrics(ratio_data):
    """Tính các chỉ số sinh lời"""
    if ratio_data.empty:
        return pd.DataFrame()
    
    metrics = {}
    try:
        metrics['roe'] = ratio_data['roe']
        metrics['roa'] = ratio_data['roa']
        metrics['profit_margin'] = ratio_data['net_profit_margin']
    except KeyError as e:
        print(f"Không tìm thấy cột dữ liệu: {str(e)}")
        return pd.DataFrame()
    
    return pd.DataFrame(metrics)

def calculate_industry_metrics(stocks_data):
    """Tính các chỉ số trung bình ngành"""
    if stocks_data.empty:
        return pd.Series()
    
    metrics = {}
    try:
        metrics['avg_pe'] = stocks_data['pe'].mean()
        metrics['avg_roe'] = stocks_data['roe'].mean()
        metrics['avg_market_cap'] = stocks_data['marketCap'].mean()
    except KeyError as e:
        print(f"Không tìm thấy cột dữ liệu: {str(e)}")
        return pd.Series()
    
    return pd.Series(metrics)

def calculate_risk_metrics(price_data):
    """Tính các chỉ số rủi ro"""
    if price_data.empty:
        return pd.Series()
    
    metrics = {}
    try:
        returns = price_data['close'].pct_change()
        metrics['volatility'] = returns.std() * np.sqrt(252) * 100  # Độ biến động hàng năm
        metrics['max_drawdown'] = (price_data['close'].max() - price_data['close'].min()) / price_data['close'].max() * 100
    except KeyError as e:
        print(f"Không tìm thấy cột dữ liệu: {str(e)}")
        return pd.Series()
    
    return pd.Series(metrics)

def simple_price_forecast(price_data, days=5):
    """Dự báo giá đơn giản dựa trên xu hướng"""
    if price_data.empty or len(price_data) < 2:
        return pd.DataFrame()
    
    try:
        returns = price_data['close'].pct_change()
        avg_return = returns.mean()
        last_price = price_data['close'].iloc[-1]
        
        forecast = []
        for i in range(1, days + 1):
            forecast_price = last_price * (1 + avg_return) ** i
            forecast.append({
                'date': (price_data.index[-1] + timedelta(days=i)).strftime('%Y-%m-%d'),
                'forecast_price': forecast_price
            })
        
        return pd.DataFrame(forecast)
    except Exception as e:
        print(f"Lỗi trong quá trình dự báo: {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
    try:
        advanced_features_example()
        print("\nVí dụ hoàn thành thành công!")
    except Exception as e:
        print(f"\nLỗi trong quá trình chạy ví dụ: {str(e)}") 