# Database Schema

*Cập nhật lần cuối: 2024-03-19*

## 1. Tổng quan

Hệ thống sử dụng MySQL làm database chính:
1. **MySQL 8.0**: Lưu trữ tất cả dữ liệu (users, strategies, portfolios, price data)
2. **File-based Cache**: Cache dữ liệu thường xuyên truy cập

## 2. Các Bảng Chính

### 2.1 Users
```sql
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.2 Stocks
```sql
CREATE TABLE stocks (
    id CHAR(36) PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    exchange VARCHAR(10) NOT NULL,
    industry VARCHAR(100),
    sector VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.3 Price Data
```sql
CREATE TABLE price_data (
    stock_id CHAR(36),
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(20,2),
    high DECIMAL(20,2),
    low DECIMAL(20,2),
    close DECIMAL(20,2),
    volume BIGINT,
    PRIMARY KEY (stock_id, timestamp),
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.4 Financial Data
```sql
CREATE TABLE financial_data (
    stock_id CHAR(36),
    period DATE NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (stock_id, period, report_type),
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.5 Strategies
```sql
CREATE TABLE strategies (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    parameters JSON,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.6 Backtests
```sql
CREATE TABLE backtests (
    id CHAR(36) PRIMARY KEY,
    strategy_id CHAR(36),
    user_id CHAR(36),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    initial_capital DECIMAL(20,2) NOT NULL,
    parameters JSON,
    results JSON,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (strategy_id) REFERENCES strategies(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.7 Portfolios
```sql
CREATE TABLE portfolios (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    initial_capital DECIMAL(20,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2.8 Positions
```sql
CREATE TABLE positions (
    id CHAR(36) PRIMARY KEY,
    portfolio_id CHAR(36),
    stock_id CHAR(36),
    entry_date TIMESTAMP NOT NULL,
    exit_date TIMESTAMP NULL,
    quantity INTEGER NOT NULL,
    entry_price DECIMAL(20,2) NOT NULL,
    exit_price DECIMAL(20,2) NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 3. Indexes

### 3.1 Price Data Indexes
```sql
-- Index cho truy vấn theo thời gian
CREATE INDEX idx_price_data_timestamp ON price_data (timestamp DESC);

-- Index cho truy vấn theo stock và thời gian
CREATE INDEX idx_price_data_stock_timestamp ON price_data (stock_id, timestamp DESC);
```

### 3.2 Financial Data Indexes
```sql
CREATE INDEX idx_financial_data_stock_period ON financial_data (stock_id, period DESC);
CREATE INDEX idx_financial_data_report_type ON financial_data (report_type);
```

### 3.3 Strategy Indexes
```sql
CREATE INDEX idx_strategies_user ON strategies (user_id);
CREATE INDEX idx_strategies_public ON strategies (is_public) WHERE is_public = TRUE;
```

### 3.4 Backtest Indexes
```sql
CREATE INDEX idx_backtests_strategy ON backtests (strategy_id);
CREATE INDEX idx_backtests_user ON backtests (user_id);
CREATE INDEX idx_backtests_status ON backtests (status);
```

## 4. Views

### 4.1 Stock Performance View
```sql
CREATE VIEW stock_performance AS
SELECT 
    s.symbol,
    s.name,
    pd.timestamp,
    pd.close,
    pd.volume,
    LAG(pd.close) OVER (PARTITION BY s.id ORDER BY pd.timestamp) as prev_close,
    (pd.close - LAG(pd.close) OVER (PARTITION BY s.id ORDER BY pd.timestamp)) / 
    LAG(pd.close) OVER (PARTITION BY s.id ORDER BY pd.timestamp) * 100 as daily_return
FROM stocks s
JOIN price_data pd ON s.id = pd.stock_id;
```

### 4.2 Portfolio Performance View
```sql
CREATE VIEW portfolio_performance AS
SELECT 
    p.id as portfolio_id,
    p.name as portfolio_name,
    pos.entry_date,
    pos.exit_date,
    s.symbol,
    pos.quantity,
    pos.entry_price,
    pos.exit_price,
    (pos.exit_price - pos.entry_price) * pos.quantity as pnl
FROM portfolios p
JOIN positions pos ON p.id = pos.portfolio_id
JOIN stocks s ON pos.stock_id = s.id;
```

## 5. Functions

### 5.1 Calculate Technical Indicators
```sql
DELIMITER //

CREATE FUNCTION calculate_technical_indicators(
    p_stock_id CHAR(36),
    p_start_date TIMESTAMP,
    p_end_date TIMESTAMP
) RETURNS TABLE (
    timestamp TIMESTAMP,
    sma_20 DECIMAL(20,2),
    sma_50 DECIMAL(20,2),
    rsi_14 DECIMAL(20,2),
    macd DECIMAL(20,2),
    macd_signal DECIMAL(20,2)
)
BEGIN
    RETURN (
        WITH price_data AS (
            SELECT 
                timestamp,
                close,
                LAG(close, 20) OVER (ORDER BY timestamp) as lag_20,
                LAG(close, 50) OVER (ORDER BY timestamp) as lag_50
            FROM price_data
            WHERE stock_id = p_stock_id
            AND timestamp BETWEEN p_start_date AND p_end_date
        )
        SELECT 
            pd.timestamp,
            AVG(pd.close) OVER (ORDER BY pd.timestamp ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as sma_20,
            AVG(pd.close) OVER (ORDER BY pd.timestamp ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) as sma_50,
            -- RSI calculation
            CASE 
                WHEN AVG(CASE WHEN pd.close > pd.lag_20 THEN pd.close - pd.lag_20 ELSE 0 END) OVER 
                    (ORDER BY pd.timestamp ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) = 0 THEN 100
                ELSE 100 - (100 / (1 + 
                    AVG(CASE WHEN pd.close > pd.lag_20 THEN pd.close - pd.lag_20 ELSE 0 END) OVER 
                        (ORDER BY pd.timestamp ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) /
                    AVG(CASE WHEN pd.close < pd.lag_20 THEN pd.lag_20 - pd.close ELSE 0 END) OVER 
                        (ORDER BY pd.timestamp ROWS BETWEEN 13 PRECEDING AND CURRENT ROW)
                ))
            END as rsi_14,
            -- MACD calculation (simplified)
            AVG(pd.close) OVER (ORDER BY pd.timestamp ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) -
            AVG(pd.close) OVER (ORDER BY pd.timestamp ROWS BETWEEN 25 PRECEDING AND CURRENT ROW) as macd,
            AVG(pd.close) OVER (ORDER BY pd.timestamp ROWS BETWEEN 8 PRECEDING AND CURRENT ROW) as macd_signal
        FROM price_data pd
    );
END //

DELIMITER ;
```

## 6. Lưu ý khi Sử dụng

1. **MySQL**:
   - Sử dụng InnoDB engine cho transaction và foreign key
   - Sử dụng utf8mb4_unicode_ci cho hỗ trợ Unicode đầy đủ
   - Tận dụng các index phù hợp
   - Sử dụng JSON type cho dữ liệu động
   - Sử dụng TIMESTAMP với ON UPDATE CURRENT_TIMESTAMP cho các trường updated_at

2. **File-based Cache**:
   - Cache dữ liệu thường xuyên truy cập
   - Sử dụng thư mục cache/ để lưu trữ
   - Implement cache invalidation strategy
   - Backup cache files định kỳ

3. **Backup & Recovery**:
   - Sử dụng mysqldump để backup database
   - Backup file-based cache
   - Test recovery process định kỳ 