#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kiểm tra cấu trúc dữ liệu trả về của các hàm trong vnstock
"""

import logging
from vnstock import *
import pandas as pd
from datetime import datetime, timedelta

# Configure pandas to handle deprecation warnings
pd.set_option('future.no_silent_downcasting', True)
pd.set_option('mode.copy_on_write', True)  # Enable new DataFrame manipulation behavior

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_basic_functions():
    """Test basic stock data retrieval functions"""
    try:
        print("Testing basic functions...")
        
        # Test listing companies
        listing = Listing()
        companies = listing.all_symbols()
        print(f"Found {len(companies)} listed companies")
        
        # Test historical data
        stock = Vnstock().stock(symbol='ACB', source='VCI')
        hist_data = stock.quote.history(
            start='2024-01-01',
            end='2024-03-19',
            interval='1D'
        )
        hist_data = hist_data.infer_objects(copy=False)
        print(f"Historical data shape: {hist_data.shape}")
        
        # Test company overview
        company = stock.company
        overview = company.overview()
        overview = overview.infer_objects(copy=False)
        print(f"Company overview data retrieved for ACB")
        
    except Exception as e:
        logger.error(f"Error in test_basic_functions: {str(e)}")
        raise

def test_screener():
    """Test stock screener functionality"""
    try:
        print("\nTesting screener functions...")
        
        # Test stock screener
        stock = Vnstock().stock(symbol='ACB', source='VCI')
        screener_data = stock.screener.stock(
            params={"exchangeName": "HOSE,HNX,UPCOM"},
            limit=1700
        )
        if screener_data is not None:
            screener_data = screener_data.infer_objects(copy=False)
        print(f"Screener data shape: {screener_data.shape if screener_data is not None else 'No data'}")
        
    except Exception as e:
        logger.error(f"Error in test_screener: {str(e)}")
        raise

def test_advanced_functions():
    """Test advanced financial data retrieval functions"""
    try:
        print("\nTesting advanced functions...")
        
        stock = Vnstock().stock(symbol='ACB', source='VCI')
        
        # Test financial reports
        balance_sheet = stock.finance.balance_sheet(
            period='year',
            lang='vi',
            dropna=True
        )
        balance_sheet = balance_sheet.infer_objects(copy=False)
        print("Balance sheet data retrieved")
        
        income_stmt = stock.finance.income_statement(
            period='year',
            lang='vi',
            dropna=True
        )
        income_stmt = income_stmt.infer_objects(copy=False)
        print("Income statement data retrieved")
        
        cash_flow = stock.finance.cash_flow(
            period='year',
            dropna=True
        )
        cash_flow = cash_flow.infer_objects(copy=False)
        print("Cash flow data retrieved")
        
        ratios = stock.finance.ratio(
            period='year',
            lang='vi',
            dropna=True
        )
        ratios = ratios.infer_objects(copy=False)
        print("Financial ratios retrieved")
        
        # Test intraday data
        intraday = stock.quote.intraday(
            symbol='ACB',
            page_size=10_000,
            show_log=False
        )
        if intraday is not None:
            intraday = intraday.infer_objects(copy=False)
        print(f"Intraday data shape: {intraday.shape if intraday is not None else 'No data'}")
        
    except Exception as e:
        logger.error(f"Error in test_advanced_functions: {str(e)}")
        raise

if __name__ == "__main__":
    print("Starting to test vnstock functions...")
    test_basic_functions()
    test_screener()
    test_advanced_functions()
    print("\nFinished testing vnstock functions.") 