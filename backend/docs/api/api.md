# API Documentation
*Cập nhật lần cuối: 2024-04-18*

## Tổng quan
API của Stock Analysis & Backtesting Platform được xây dựng trên FastAPI, cung cấp các endpoints để truy cập dữ liệu chứng khoán, quản lý danh mục đầu tư, và thực hiện backtesting chiến lược.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
API sử dụng JWT (JSON Web Token) cho xác thực. Để truy cập các endpoint được bảo vệ, bạn cần gửi token trong header:

```
Authorization: Bearer <your_token>
```

## Endpoints

### 1. Authentication

#### 1.1 Đăng ký
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "full_name": "string"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "username": "string",
  "email": "user@example.com",
  "full_name": "string",
  "created_at": "2024-04-18T12:00:00Z"
}
```

#### 1.2 Đăng nhập
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 1800,
  "refresh_token": "string"
}
```

#### 1.3 Làm mới token
```http
POST /auth/refresh
```

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. Users

#### 2.1 Lấy thông tin người dùng
```http
GET /users/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "string",
  "username": "string",
  "email": "user@example.com",
  "full_name": "string",
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z"
}
```

#### 2.2 Cập nhật thông tin người dùng
```http
PUT /users/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "full_name": "string",
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "username": "string",
  "email": "user@example.com",
  "full_name": "string",
  "updated_at": "2024-04-18T12:00:00Z"
}
```

#### 2.3 Đổi mật khẩu
```http
PUT /users/me/password
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Password updated successfully"
}
```

### 3. Stocks

#### 3.1 Lấy danh sách cổ phiếu
```http
GET /stocks
```

**Query Parameters:**
- `page` (int, optional): Số trang (mặc định: 1)
- `limit` (int, optional): Số lượng kết quả mỗi trang (mặc định: 20)
- `search` (string, optional): Tìm kiếm theo mã hoặc tên
- `sector` (string, optional): Lọc theo ngành

**Response (200 OK):**
```json
{
  "items": [
    {
      "symbol": "string",
      "name": "string",
      "sector": "string",
      "market_cap": 1000000000,
      "current_price": 100.5,
      "change_percent": 1.5
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

#### 3.2 Lấy thông tin chi tiết cổ phiếu
```http
GET /stocks/{symbol}
```

**Response (200 OK):**
```json
{
  "symbol": "string",
  "name": "string",
  "sector": "string",
  "market_cap": 1000000000,
  "current_price": 100.5,
  "change_percent": 1.5,
  "volume": 1000000,
  "pe_ratio": 15.5,
  "pb_ratio": 2.5,
  "dividend_yield": 3.5,
  "description": "string",
  "financials": {
    "revenue": 1000000000,
    "profit": 100000000,
    "assets": 2000000000,
    "liabilities": 1000000000
  }
}
```

#### 3.3 Lấy dữ liệu giá lịch sử
```http
GET /stocks/{symbol}/prices
```

**Query Parameters:**
- `start_date` (string, optional): Ngày bắt đầu (YYYY-MM-DD)
- `end_date` (string, optional): Ngày kết thúc (YYYY-MM-DD)
- `interval` (string, optional): Khoảng thời gian (1d, 1w, 1m)

**Response (200 OK):**
```json
{
  "symbol": "string",
  "prices": [
    {
      "date": "2024-04-18",
      "open": 100.5,
      "high": 101.5,
      "low": 99.5,
      "close": 100.5,
      "volume": 1000000
    }
  ]
}
```

#### 3.4 Lấy dữ liệu tài chính
```http
GET /stocks/{symbol}/financials
```

**Query Parameters:**
- `year` (int, optional): Năm tài chính
- `quarter` (int, optional): Quý (1-4)

**Response (200 OK):**
```json
{
  "symbol": "string",
  "financials": [
    {
      "year": 2023,
      "quarter": 4,
      "revenue": 1000000000,
      "profit": 100000000,
      "eps": 2.5,
      "roe": 15.5,
      "debt_to_equity": 0.5
    }
  ]
}
```

### 4. Portfolios

#### 4.1 Lấy danh sách danh mục
```http
GET /portfolios
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "created_at": "2024-04-18T12:00:00Z",
      "updated_at": "2024-04-18T12:00:00Z",
      "total_value": 10000000,
      "return_percent": 5.5
    }
  ],
  "total": 5
}
```

#### 4.2 Tạo danh mục mới
```http
POST /portfolios
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "string",
  "description": "string"
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z",
  "total_value": 0,
  "return_percent": 0
}
```

#### 4.3 Cập nhật danh mục
```http
PUT /portfolios/{portfolio_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "string",
  "description": "string"
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z",
  "total_value": 10000000,
  "return_percent": 5.5
}
```

#### 4.4 Xóa danh mục
```http
DELETE /portfolios/{portfolio_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

#### 4.5 Thêm cổ phiếu vào danh mục
```http
POST /portfolios/{portfolio_id}/stocks
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "symbol": "string",
  "quantity": 100,
  "price": 100.5
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "symbol": "string",
  "name": "string",
  "quantity": 100,
  "avg_price": 100.5,
  "current_price": 105.5,
  "value": 10550,
  "return_percent": 5.0
}
```

#### 4.6 Cập nhật cổ phiếu trong danh mục
```http
PUT /portfolios/{portfolio_id}/stocks/{stock_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "quantity": 150
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "symbol": "string",
  "name": "string",
  "quantity": 150,
  "avg_price": 100.5,
  "current_price": 105.5,
  "value": 15825,
  "return_percent": 5.0
}
```

#### 4.7 Xóa cổ phiếu khỏi danh mục
```http
DELETE /portfolios/{portfolio_id}/stocks/{stock_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

### 5. Strategies

#### 5.1 Lấy danh sách chiến lược
```http
GET /strategies
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "created_at": "2024-04-18T12:00:00Z",
      "updated_at": "2024-04-18T12:00:00Z",
      "parameters": {
        "ma_period": 20,
        "rsi_period": 14,
        "rsi_overbought": 70,
        "rsi_oversold": 30
      }
    }
  ],
  "total": 5
}
```

#### 5.2 Tạo chiến lược mới
```http
POST /strategies
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "parameters": {
    "ma_period": 20,
    "rsi_period": 14,
    "rsi_overbought": 70,
    "rsi_oversold": 30
  }
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z",
  "parameters": {
    "ma_period": 20,
    "rsi_period": 14,
    "rsi_overbought": 70,
    "rsi_oversold": 30
  }
}
```

#### 5.3 Cập nhật chiến lược
```http
PUT /strategies/{strategy_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "parameters": {
    "ma_period": 10,
    "rsi_period": 20
  }
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z",
  "parameters": {
    "ma_period": 10,
    "rsi_period": 20
  }
}
```

#### 5.4 Xóa chiến lược
```http
DELETE /strategies/{strategy_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

### 6. Backtests

#### 6.1 Lấy danh sách backtest
```http
GET /strategies/{strategy_id}/backtests
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "symbol": "string",
      "start_date": "2023-01-01",
      "end_date": "2023-12-31",
      "initial_capital": 10000000,
      "final_capital": 12000000,
      "return_percent": 20.0,
      "max_drawdown": 10.0,
      "sharpe_ratio": 1.5,
      "created_at": "2024-04-18T12:00:00Z"
    }
  ],
  "total": 10
}
```

#### 6.2 Tạo backtest mới
```http
POST /strategies/{strategy_id}/backtest
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "symbol": "string",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_capital": 10000000,
  "parameters": {
    "ma_period": 20,
    "rsi_period": 14
  }
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "strategy_id": "string",
  "symbol": "string",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_capital": 10000000,
  "final_capital": 12000000,
  "return_percent": 20.0,
  "max_drawdown": 10.0,
  "sharpe_ratio": 1.5,
  "trades": [
    {
      "date": "2023-01-15",
      "type": "buy",
      "price": 100.5,
      "quantity": 100,
      "value": 10050
    }
  ],
  "equity_curve": [
    {
      "date": "2023-01-01",
      "value": 10000000
    }
  ],
  "created_at": "2024-04-18T12:00:00Z"
}
```

#### 6.3 Lấy chi tiết backtest
```http
GET /backtests/{backtest_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "string",
  "strategy_id": "string",
  "strategy_name": "string",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_capital": 10000000,
  "final_capital": 12000000,
  "return_percent": 20.0,
  "max_drawdown": 10.0,
  "sharpe_ratio": 1.5,
  "parameters": {
    "ma_period": 20,
    "rsi_period": 14
  },
  "results": {
    "trades": [
      {
        "date": "2023-01-15",
        "type": "buy",
        "price": 100.5,
        "quantity": 100,
        "value": 10050
      }
    ],
    "equity_curve": [
      {
        "date": "2023-01-01",
        "value": 10000000
      }
    ]
  },
  "created_at": "2024-04-18T12:00:00Z"
}
```

### 7. Alerts

#### 7.1 Lấy danh sách cảnh báo
```http
GET /alerts
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "string",
      "symbol": "string",
      "name": "string",
      "condition": "price > 100",
      "value": 100,
      "is_active": true,
      "created_at": "2024-04-18T12:00:00Z",
      "updated_at": "2024-04-18T12:00:00Z",
      "last_triggered": "2024-04-18T12:00:00Z"
    }
  ],
  "total": 5
}
```

#### 7.2 Tạo cảnh báo mới
```http
POST /alerts
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "symbol": "string",
  "name": "string",
  "condition": "price > 100",
  "value": 100
}
```

**Response (201 Created):**
```json
{
  "id": "string",
  "symbol": "string",
  "name": "string",
  "condition": "price > 100",
  "value": 100,
  "is_active": true,
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z"
}
```

#### 7.3 Cập nhật cảnh báo
```http
PUT /alerts/{alert_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "string",
  "condition": "price > 110",
  "value": 110,
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id": "string",
  "symbol": "string",
  "name": "string",
  "condition": "price > 110",
  "value": 110,
  "is_active": true,
  "created_at": "2024-04-18T12:00:00Z",
  "updated_at": "2024-04-18T12:00:00Z",
  "last_triggered": "2024-04-18T12:00:00Z"
}
```

#### 7.4 Xóa cảnh báo
```http
DELETE /alerts/{alert_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to access this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "Resource already exists"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting
API có giới hạn số lượng request:
- 100 requests/phút cho các endpoints không yêu cầu xác thực
- 1000 requests/phút cho các endpoints yêu cầu xác thực

## Pagination
Các endpoints trả về danh sách đều hỗ trợ phân trang:
- `page`: Số trang (bắt đầu từ 1)
- `limit`: Số lượng kết quả mỗi trang (mặc định là 20, tối đa là 100)

## Versioning
API sử dụng versioning trong URL path:
- Hiện tại: `/api/v1`
- Các phiên bản mới sẽ được đánh số tăng dần: `/api/v2`, `/api/v3`, ...

## Ghi chú
- Tất cả các request và response đều sử dụng định dạng JSON
- Timestamps được trả về theo định dạng ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`
- Các giá trị tiền tệ được trả về theo đơn vị VND (không có phần thập phân)
- Các giá trị phần trăm được trả về với 2 chữ số thập phân 