# vnstock Library Demo

Thư viện vnstock cung cấp giao diện Python để truy cập dữ liệu thị trường chứng khoán Việt Nam từ nhiều nguồn khác nhau.

## Thông tin Phiên bản
- Thư viện: vnstock >= 3.0.0
- Python: >= 3.7
- Cập nhật lần cuối: 2024-04-18

## Cấu trúc Thư mục

```
vnstock/
├── README.md           # Tài liệu tổng quan
├── api_reference.md    # Tài liệu chi tiết về API
├── examples/          # Thư mục chứa các ví dụ
│   ├── basic_usage.py
│   ├── historical_data.py
│   ├── company_info.py
│   ├── financial_data.py
│   ├── stock_screening.py
│   └── advanced_features.py
└── requirements.txt   # Các dependencies cần thiết
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Các Tính năng Chính

1. **Dữ liệu Giá Lịch sử**
   - Lấy dữ liệu OHLCV theo nhiều khung thời gian
   - Dữ liệu trong ngày (intraday)
   - Bảng giá thời gian thực

2. **Thông tin Công ty**
   - Thông tin tổng quan
   - Hồ sơ công ty
   - Ban lãnh đạo

3. **Dữ liệu Tài chính**
   - Bảng cân đối kế toán
   - Báo cáo kết quả kinh doanh
   - Báo cáo lưu chuyển tiền tệ
   - Các chỉ số tài chính

4. **Bộ lọc Cổ phiếu**
   - Lọc theo nhiều tiêu chí
   - Phân tích kỹ thuật
   - Phân tích cơ bản

## Cách Sử dụng

### 1. Giao diện Hợp nhất (Khuyến nghị)

```python
from vnstock import Vnstock

# Khởi tạo đối tượng
stock = Vnstock().stock(symbol='VCI', source='VCI')

# Lấy dữ liệu giá
history = stock.quote.history(
    start_date='2024-01-01',
    end_date='2024-03-25',
    resolution='1D'
)

# Lấy thông tin công ty
overview = stock.company.overview()

# Lấy báo cáo tài chính
balance_sheet = stock.finance.balance_sheet(period='year')
```

### 2. Sử dụng Lớp Riêng lẻ

```python
from vnstock import Quote, Company, Finance

# Khởi tạo các lớp riêng lẻ
quote = Quote(symbol='VCI', source='VCI')
company = Company(symbol='VCI', source='VCI')
finance = Finance(symbol='VCI', source='VCI')

# Sử dụng các phương thức
history = quote.history(start_date='2024-01-01', end_date='2024-03-25')
overview = company.overview()
ratios = finance.ratio(period='quarter')
```

## Các Ví dụ

Xem thư mục `examples/` để biết các ví dụ chi tiết về:
- Sử dụng cơ bản
- Lấy dữ liệu lịch sử
- Truy cập thông tin công ty
- Phân tích tài chính
- Bộ lọc cổ phiếu
- Các tính năng nâng cao

## Nguồn Dữ liệu

vnstock hỗ trợ nhiều nguồn dữ liệu:
- DNSE (mặc định)
- TCBS
- VCI
- SSI
- VND
- HSC

## Hạn chế và Giới hạn

1. **Rate Limiting**
   - DNSE: 100 requests/phút
   - TCBS: 50 requests/phút
   - VCI: 30 requests/phút
   - Các nguồn khác: 20 requests/phút

2. **Giới hạn Dữ liệu**
   - Dữ liệu lịch sử: Tối đa 5 năm
   - Dữ liệu intraday: Tối đa 30 ngày
   - Báo cáo tài chính: Tối đa 10 năm

3. **Yêu cầu Tài khoản**
   - TCBS, VCI, SSI, VND, HSC yêu cầu tài khoản
   - DNSE không yêu cầu tài khoản

## Best Practices

1. **Sử dụng Giao diện Hợp nhất**
   - Code sạch sẽ hơn
   - Dễ bảo trì
   - Hiệu quả hơn

2. **Xử lý Lỗi**
   - Luôn kiểm tra kết quả trả về
   - Xử lý các trường hợp ngoại lệ
   - Log lỗi đầy đủ

3. **Tối ưu Hiệu năng**
   - Cache dữ liệu khi cần
   - Sử dụng batch requests
   - Giới hạn tần suất gọi API
   - Sử dụng rate limiting phù hợp

## Tài liệu Tham khảo

- [GitHub Repository](https://github.com/thinh-vu/vnstock)
- [API Documentation](api_reference.md)
- [Ví dụ Code](examples/) 