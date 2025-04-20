import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from vnstock import Vnstock, Listing
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StockDataService:
    """Service for retrieving stock market data"""
    
    def __init__(self):
        """Initialize the service"""
        self.listing = Listing()
        
    def get_stock_list(self) -> List[Dict[str, Any]]:
        """Get list of all available stocks
        
        Returns:
            List[Dict[str, Any]]: List of stocks with their basic information
        """
        try:
            stocks = self.listing.all_symbols()
            if stocks is not None:
                stocks = pd.DataFrame(stocks)
                return stocks.to_dict('records')
            return []
        except Exception as e:
            logger.error(f"Error getting stock list: {str(e)}")
            raise
    
    def get_stock_price(self, symbol: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get historical price data for a stock
        
        Args:
            symbol (str): Stock symbol
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Historical price data
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get historical data
            hist_data = stock.quote.history(
                start=start_date,
                end=end_date,
                interval='1D'
            )
            
            if hist_data is not None:
                hist_data = hist_data.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": hist_data.to_dict('records')
                }
            return {
                "symbol": symbol,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting price data for {symbol}: {str(e)}")
            raise
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get company information for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Company information
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get company overview
            overview = stock.company.overview()
            
            if overview is not None:
                overview = overview.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": overview.to_dict('records')[0] if len(overview) > 0 else {}
                }
            return {
                "symbol": symbol,
                "data": {}
            }
        except Exception as e:
            logger.error(f"Error getting company info for {symbol}: {str(e)}")
            raise
    
    def get_stock_basic_info(self, symbol: str) -> Dict[str, Any]:
        """Get basic company information for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Basic company information
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get basic company info using overview()
            basic_info = stock.company.overview()
            
            if basic_info is not None:
                basic_info = basic_info.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": basic_info.to_dict('records')[0] if len(basic_info) > 0 else {}
                }
            return {
                "symbol": symbol,
                "data": {}
            }
        except Exception as e:
            logger.error(f"Error getting basic company info for {symbol}: {str(e)}")
            raise
    
    def get_stock_management(self, symbol: str) -> Dict[str, Any]:
        """Get management information for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Management information
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get management info using officers()
            management = stock.company.officers()
            
            if management is not None:
                management = management.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": management.to_dict('records') if len(management) > 0 else []
                }
            return {
                "symbol": symbol,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting management info for {symbol}: {str(e)}")
            raise
    
    def get_stock_major_shareholders(self, symbol: str) -> Dict[str, Any]:
        """Get major shareholders information for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Major shareholders information
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get major shareholders info using shareholders()
            major_shareholders = stock.company.shareholders()
            
            if major_shareholders is not None:
                major_shareholders = major_shareholders.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": major_shareholders.to_dict('records') if len(major_shareholders) > 0 else []
                }
            return {
                "symbol": symbol,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting major shareholders info for {symbol}: {str(e)}")
            raise
    
    def get_stock_dividend_history(self, symbol: str) -> Dict[str, Any]:
        """Get dividend history for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Dividend history
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='TCBS')
            
            # Get dividend history using dividends()
            dividend_history = stock.company.dividends()
            
            if dividend_history is not None:
                dividend_history = dividend_history.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": dividend_history.to_dict('records') if len(dividend_history) > 0 else []
                }
            return {
                "symbol": symbol,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting dividend history for {symbol}: {str(e)}")
            raise
    
    def get_stock_events(self, symbol: str) -> Dict[str, Any]:
        """Get events for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Events information
        """
        try:
            # Initialize stock with TCBS source for better event data
            stock = Vnstock().stock(symbol=symbol, source='TCBS')
            
            # Get events
            events = stock.company.events()
            
            if events is not None:
                events = events.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "data": events.to_dict('records') if len(events) > 0 else []
                }
            return {
                "symbol": symbol,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting events for {symbol}: {str(e)}")
            raise
    
    def get_stock_financials(self, symbol: str, report_type: str = 'balance_sheet', period: str = 'year', lang: str = 'vi') -> Dict[str, Any]:
        """Get financial statements for a stock
        
        Args:
            symbol (str): Stock symbol
            report_type (str): Type of financial statement (balance_sheet, income_statement, cash_flow)
            period (str): Period of the report (year, quarter)
            lang (str): Language of the report (vi, en)
            
        Returns:
            Dict[str, Any]: Financial statements data
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get financial data using the appropriate method
            if report_type == 'balance_sheet':
                data = stock.finance.balance_sheet(period=period, lang=lang)
            elif report_type == 'income_statement':
                data = stock.finance.income_statement(period=period, lang=lang)
            elif report_type == 'cash_flow':
                data = stock.finance.cash_flow(period=period, lang=lang)
            else:
                data = stock.finance.balance_sheet(period=period, lang=lang)
            
            if data is not None:
                data = data.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "report_type": report_type,
                    "period": period,
                    "data": data.to_dict('records')
                }
            return {
                "symbol": symbol,
                "report_type": report_type,
                "period": period,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting financial data for {symbol}: {str(e)}")
            raise
    
    def get_financial_ratio(self, symbol: str, period: str = 'year') -> Dict[str, Any]:
        """Get financial ratios for a stock
        
        Args:
            symbol (str): Stock symbol
            period (str): Report period ('year', 'quarter')
            
        Returns:
            Dict[str, Any]: Financial ratio data
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get financial ratios
            data = stock.finance.financial_ratio(period=period)
            
            if data is not None:
                data = data.infer_objects(copy=False)
                return {
                    "symbol": symbol,
                    "period": period,
                    "data": data.to_dict('records')
                }
            return {
                "symbol": symbol,
                "period": period,
                "data": []
            }
        except Exception as e:
            logger.error(f"Error getting financial ratio for {symbol}: {str(e)}")
            raise
    
    def screen_stocks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Screen stocks based on criteria
        
        Args:
            limit (int): Maximum number of stocks to return
            
        Returns:
            List[Dict[str, Any]]: List of screened stocks with basic information
        """
        try:
            # Get all stocks from listing
            stocks = self.listing.all_symbols()
            
            if stocks is not None:
                stocks = pd.DataFrame(stocks)
                
                # Check if DataFrame is empty
                if stocks.empty:
                    return []
                    
                # Get available columns
                available_columns = stocks.columns.tolist()
                logger.info(f"Available columns: {available_columns}")
                
                # Select and rename columns
                columns_map = {
                    'symbol': 'symbol',
                    'organ_name': 'name'
                }
                
                # Filter columns that exist in the DataFrame
                selected_columns = {k: v for k, v in columns_map.items() if k in available_columns}
                
                # Select and rename columns
                screened_stocks = stocks[list(selected_columns.keys())].rename(columns=selected_columns)
                
                # Sort by symbol
                screened_stocks = screened_stocks.sort_values('symbol')
                
                # Limit the number of results
                if limit > 0:
                    screened_stocks = screened_stocks.head(limit)
                    
                return screened_stocks.to_dict('records')
            return []
        except Exception as e:
            logger.error(f"Error screening stocks: {str(e)}")
            raise
    
    def get_technical_analysis(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        indicators: List[str] = ["MA", "RSI", "MACD", "BB"]
    ) -> Dict[str, Any]:
        """Get technical analysis for a stock
        
        Args:
            symbol (str): Stock symbol
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            indicators (List[str]): List of technical indicators to calculate
            
        Returns:
            Dict[str, Any]: Technical analysis data
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get historical data
            hist_data = stock.quote.history(
                start=start_date,
                end=end_date,
                interval='1D'
            )
            
            if hist_data is None:
                return {
                    "symbol": symbol,
                    "data": {}
                }
                
            # Calculate technical indicators
            analysis = {}
            
            if "MA" in indicators:
                # Calculate Moving Averages
                ma5 = hist_data['close'].rolling(window=5).mean()
                ma10 = hist_data['close'].rolling(window=10).mean()
                ma20 = hist_data['close'].rolling(window=20).mean()
                ma50 = hist_data['close'].rolling(window=50).mean()
                ma200 = hist_data['close'].rolling(window=200).mean()
                
                # Replace NaN with None
                analysis["MA"] = {
                    "MA5": ma5.replace({pd.NA: None, np.nan: None}).to_dict(),
                    "MA10": ma10.replace({pd.NA: None, np.nan: None}).to_dict(),
                    "MA20": ma20.replace({pd.NA: None, np.nan: None}).to_dict(),
                    "MA50": ma50.replace({pd.NA: None, np.nan: None}).to_dict(),
                    "MA200": ma200.replace({pd.NA: None, np.nan: None}).to_dict()
                }
                
            if "RSI" in indicators:
                # Calculate RSI
                delta = hist_data['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                # Replace NaN with None
                analysis["RSI"] = rsi.replace({pd.NA: None, np.nan: None}).to_dict()
                
            if "MACD" in indicators:
                # Calculate MACD
                exp1 = hist_data['close'].ewm(span=12, adjust=False).mean()
                exp2 = hist_data['close'].ewm(span=26, adjust=False).mean()
                macd = exp1 - exp2
                signal = macd.ewm(span=9, adjust=False).mean()
                # Replace NaN with None
                analysis["MACD"] = {
                    "MACD": macd.replace({pd.NA: None, np.nan: None}).to_dict(),
                    "Signal": signal.replace({pd.NA: None, np.nan: None}).to_dict()
                }
                
            if "BB" in indicators:
                # Calculate Bollinger Bands
                sma = hist_data['close'].rolling(window=20).mean()
                std = hist_data['close'].rolling(window=20).std()
                # Replace NaN with None
                analysis["BB"] = {
                    "Upper": (sma + (std * 2)).replace({pd.NA: None, np.nan: None}).to_dict(),
                    "Middle": sma.replace({pd.NA: None, np.nan: None}).to_dict(),
                    "Lower": (sma - (std * 2)).replace({pd.NA: None, np.nan: None}).to_dict()
                }
            
            return {
                "symbol": symbol,
                "data": analysis
            }
        except Exception as e:
            logger.error(f"Error getting technical analysis for {symbol}: {str(e)}")
            raise
            
    def get_fundamental_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get fundamental analysis for a stock
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Dict[str, Any]: Fundamental analysis data
        """
        try:
            # Initialize stock
            stock = Vnstock().stock(symbol=symbol, source='TCBS')
            
            # Get financial data
            analysis = {}
            
            try:
                # Get financial ratios using finance.ratios()
                ratios = stock.finance.ratios()
                analysis["financial_ratios"] = ratios.to_dict('records') if ratios is not None else []
            except Exception as e:
                logger.warning(f"Financial ratios not available for {symbol}: {str(e)}")
                analysis["financial_ratios"] = []
                
            try:
                # Get financial statements using finance.statements()
                statements = stock.finance.statements()
                if statements is not None:
                    analysis["balance_sheet"] = statements.get('balance_sheet', []).to_dict('records')
                    analysis["income_statement"] = statements.get('income_statement', []).to_dict('records')
                    analysis["cash_flow"] = statements.get('cash_flow', []).to_dict('records')
                else:
                    analysis["balance_sheet"] = []
                    analysis["income_statement"] = []
                    analysis["cash_flow"] = []
            except Exception as e:
                logger.warning(f"Financial statements not available for {symbol}: {str(e)}")
                analysis["balance_sheet"] = []
                analysis["income_statement"] = []
                analysis["cash_flow"] = []
                
            try:
                # Get valuation metrics using finance.valuation()
                valuation = stock.finance.valuation()
                analysis["valuation"] = valuation.to_dict('records') if valuation is not None else []
            except Exception as e:
                logger.warning(f"Valuation metrics not available for {symbol}: {str(e)}")
                analysis["valuation"] = []
                
            # Get additional company info
            try:
                company_info = stock.company.info()
                if company_info is not None:
                    analysis["company_info"] = company_info.to_dict('records')[0] if len(company_info) > 0 else {}
                else:
                    analysis["company_info"] = {}
            except Exception as e:
                logger.warning(f"Company info not available for {symbol}: {str(e)}")
                analysis["company_info"] = {}
            
            return {
                "symbol": symbol,
                "data": analysis
            }
        except Exception as e:
            logger.error(f"Error getting fundamental analysis for {symbol}: {str(e)}")
            raise
            
    def get_portfolio_analysis(
        self,
        symbols: List[str],
        weights: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Analyze a portfolio of stocks
        
        Args:
            symbols (List[str]): List of stock symbols
            weights (Optional[List[float]]): List of weights for each stock
            
        Returns:
            Dict[str, Any]: Portfolio analysis data
        """
        try:
            if weights is None:
                weights = [1.0 / len(symbols)] * len(symbols)
                
            # Get basic info for all stocks
            stocks_info = []
            for symbol in symbols:
                info = self.get_stock_basic_info(symbol)
                stocks_info.append(info["data"])
                
            # Calculate portfolio metrics
            total_market_cap = sum(
                float(info.get("market_cap", 0)) * weight
                for info, weight in zip(stocks_info, weights)
            )
            
            avg_pe = sum(
                float(info.get("pe", 0)) * weight
                for info, weight in zip(stocks_info, weights)
            )
            
            avg_pb = sum(
                float(info.get("pb", 0)) * weight
                for info, weight in zip(stocks_info, weights)
            )
            
            return {
                "symbols": symbols,
                "weights": weights,
                "analysis": {
                    "total_market_cap": total_market_cap,
                    "avg_pe": avg_pe,
                    "avg_pb": avg_pb,
                    "stocks": stocks_info
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing portfolio: {str(e)}")
            raise
            
    def get_portfolio_performance(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        weights: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Get performance metrics for a portfolio
        
        Args:
            symbols (List[str]): List of stock symbols
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            weights (Optional[List[float]]): List of weights for each stock
            
        Returns:
            Dict[str, Any]: Portfolio performance data
        """
        try:
            if weights is None:
                weights = [1.0 / len(symbols)] * len(symbols)
                
            # Get price data for all stocks
            portfolio_data = []
            for symbol in symbols:
                price_data = self.get_stock_price(symbol, start_date, end_date)
                portfolio_data.append(price_data["data"])
                
            # Calculate portfolio returns
            returns = []
            for data, weight in zip(portfolio_data, weights):
                if len(data) > 0:
                    start_price = float(data[0]["close"])
                    end_price = float(data[-1]["close"])
                    stock_return = (end_price - start_price) / start_price
                    weighted_return = stock_return * weight
                    returns.append(weighted_return)
                    
            total_return = sum(returns)
            
            # Calculate daily returns for volatility
            daily_returns = []
            for data, weight in zip(portfolio_data, weights):
                if len(data) > 1:
                    for i in range(1, len(data)):
                        prev_price = float(data[i-1]["close"])
                        curr_price = float(data[i]["close"])
                        daily_return = (curr_price - prev_price) / prev_price
                        daily_returns.append(daily_return * weight)
                        
            # Calculate volatility (standard deviation of daily returns)
            volatility = pd.Series(daily_returns).std()
            
            return {
                "symbols": symbols,
                "weights": weights,
                "performance": {
                    "total_return": total_return,
                    "volatility": volatility,
                    "sharpe_ratio": total_return / volatility if volatility != 0 else 0,
                    "daily_returns": daily_returns
                }
            }
        except Exception as e:
            logger.error(f"Error getting portfolio performance: {str(e)}")
            raise