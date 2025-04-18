# vnstock API Reference

Tài liệu chi tiết về các API của thư viện vnstock 3.x.

## 1. Giao diện Hợp nhất (Vnstock)

### Khởi tạo
```python
from vnstock import Vnstock
stock = Vnstock().stock(symbol='VCI', source='VCI')
```

### Các Phương thức

#### 1.1 Quote (Dữ liệu Giá)

##### history()
Lấy dữ liệu giá lịch sử.

**Tham số:**
- `start_date` (str): Ngày bắt đầu (YYYY-MM-DD)
- `end_date` (str): Ngày kết thúc (YYYY-MM-DD)
- `resolution` (str): Độ phân giải thời gian
  - '1D': Ngày
  - '1': 1 phút
  - '3': 3 phút
  - '5': 5 phút
  - '15': 15 phút
  - '30': 30 phút
  - '1H': 1 giờ
- `type` (str): Loại tài sản ('stock', 'index', 'derivative')
- `source` (str): Nguồn dữ liệu ('DNSE', 'TCBS', 'VCI', ...)
- `beautify` (bool): Làm tròn giá OHLC
- `decor` (bool): Định dạng lại cột và đặt 'Time' làm chỉ mục

**Ví dụ:**
```python
history = stock.quote.history(
    start_date='2024-01-01',
    end_date='2024-03-25',
    resolution='1D'
)
```

##### intraday()
Lấy dữ liệu trong ngày.

**Tham số:**
- `page_size` (int): Số lượng bản ghi tối đa

**Ví dụ:**
```python
intraday = stock.quote.intraday(page_size=5000)
```

#### 1.2 Company (Thông tin Công ty)

##### overview()
Lấy thông tin tổng quan về công ty.

**Ví dụ:**
```python
overview = stock.company.overview()
```

#### 1.3 Finance (Dữ liệu Tài chính)

##### balance_sheet()
Lấy bảng cân đối kế toán.

**Tham số:**
- `period` (str): Kỳ báo cáo ('year', 'quarter')
- `lang` (str): Ngôn ngữ ('vi', 'en')

**Ví dụ:**
```python
balance_sheet = stock.finance.balance_sheet(period='year', lang='vi')
```

##### income_statement()
Lấy báo cáo kết quả kinh doanh.

**Tham số:**
- `period` (str): Kỳ báo cáo ('year', 'quarter')
- `lang` (str): Ngôn ngữ ('vi', 'en')

**Ví dụ:**
```python
income = stock.finance.income_statement(period='quarter', lang='en')
```

##### cash_flow()
Lấy báo cáo lưu chuyển tiền tệ.

**Tham số:**
- `period` (str): Kỳ báo cáo ('year', 'quarter')
- `lang` (str): Ngôn ngữ ('vi', 'en')

**Ví dụ:**
```python
cash_flow = stock.finance.cash_flow(period='year', lang='vi')
```

##### ratio()
Lấy các chỉ số tài chính.

**Tham số:**
- `period` (str): Kỳ báo cáo ('year', 'quarter')
- `lang` (str): Ngôn ngữ ('vi', 'en')
- `is_all` (bool): Lấy tất cả các chỉ số

**Ví dụ:**
```python
ratios = stock.finance.ratio(period='quarter', lang='en', is_all=True)
```

## 2. Bộ lọc Cổ phiếu (Screener)

### Khởi tạo
```python
from vnstock import Screener
screener = Screener(source='TCBS')
```

### stock_screening_insights()
Lọc cổ phiếu theo các tiêu chí.

**Tham số:**
- `params` (dict): Các tiêu chí lọc
  - `exchangeName`: Sàn giao dịch ('HOSE', 'HNX', 'UPCOM')
  - `marketCap`: Vốn hóa thị trường (tỷ VND)
  - `pe`: P/E
  - `roe`: ROE (%)
  - `dividendYield`: Tỷ suất cổ tức (%)
- `size` (int): Số lượng cổ phiếu tối đa

**Ví dụ:**
```python
filters = {
    "exchangeName": "HOSE,HNX",
    "marketCap": (1000, 10000),
    "pe": (0, 15),
    "roe": (15, 100)
}
screened_stocks = screener.stock_screening_insights(params=filters, size=100)
```

## 3. Danh sách Cổ phiếu (Listing)

### Khởi tạo
```python
from vnstock import Listing
listing = Listing()
```

### all_symbols()
Lấy danh sách tất cả mã cổ phiếu.

**Ví dụ:**
```python
symbols = listing.all_symbols()
```

## 4. Các Nguồn Dữ liệu

### DNSE (Mặc định)
- Dữ liệu cơ bản
- Giới hạn lịch sử
- Miễn phí

### TCBS
- Dữ liệu nâng cao
- Bộ lọc cổ phiếu
- Yêu cầu tài khoản

### VCI
- Dữ liệu thời gian thực
- Thông tin chi tiết công ty
- Yêu cầu tài khoản

### Các nguồn khác
- SSI
- VND
- HSC

## 5. Xử lý Lỗi

Các lỗi phổ biến:
- `ConnectionError`: Lỗi kết nối
- `TimeoutError`: Quá thời gian chờ
- `ValueError`: Tham số không hợp lệ
- `APIError`: Lỗi từ API

**Ví dụ xử lý lỗi:**
```python
try:
    data = stock.quote.history(...)
except ConnectionError as e:
    print(f"Lỗi kết nối: {e}")
except TimeoutError as e:
    print(f"Quá thời gian chờ: {e}")
except Exception as e:
    print(f"Lỗi không xác định: {e}")
``` 