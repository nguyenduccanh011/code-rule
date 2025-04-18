# Cấu trúc Dữ liệu Trả về của vnstock

*Cập nhật lần cuối: 2024-03-19*
*Phiên bản vnstock: 3.2.0*

## 1. Basic Functions

### 1.1 Listing Companies
```python
listing = Listing()
companies = listing.all_symbols()
```
- **Kiểu dữ liệu**: List
- **Số lượng**: 1709 công ty
- **Cấu trúc**: Danh sách các mã cổ phiếu
- **Ví dụ**: ['ACB', 'BID', 'CTG', 'FPT', 'GAS', ...]

### 1.2 Historical Data
```python
stock = Vnstock().stock(symbol='ACB', source='VCI')
hist_data = stock.quote.history(
    start='2024-01-01',
    end='2024-03-19',
    interval='1D'
)
```
- **Kiểu dữ liệu**: DataFrame
- **Kích thước**: (51, 6)
- **Các cột**:
  - date: Ngày giao dịch (datetime64[ns])
  - open: Giá mở cửa (float64)
  - high: Giá cao nhất (float64)
  - low: Giá thấp nhất (float64)
  - close: Giá đóng cửa (float64)
  - volume: Khối lượng giao dịch (int64)
- **Tham số tùy chọn**:
  - interval: '1D' (ngày), '1W' (tuần), '1M' (tháng)
  - source: 'VCI', 'TCBS', 'SSI'

### 1.3 Company Overview
```python
company = stock.company
overview = company.overview()
```
- **Kiểu dữ liệu**: DataFrame
- **Cấu trúc**: Thông tin tổng quan về công ty
- **Các trường thông tin**:
  - ticker: Mã cổ phiếu (str)
  - companyName: Tên công ty (str)
  - industry: Ngành nghề (str)
  - exchange: Sàn giao dịch (str)
  - charterCapital: Vốn điều lệ (float)
  - outstandingShares: Cổ phiếu đang lưu hành (int)
  - listingDate: Ngày niêm yết (datetime)
  - website: Website công ty (str)
  - address: Địa chỉ (str)

## 2. Screener Functions

### 2.1 Stock Screener
```python
screener_data = stock.screener.stock(
    params={"exchangeName": "HOSE,HNX,UPCOM"},
    limit=1700
)
```
- **Kiểu dữ liệu**: DataFrame
- **Kích thước**: (1613, 83)
- **Các cột chính**:
  - ticker: Mã cổ phiếu (str)
  - companyName: Tên công ty (str)
  - price: Giá hiện tại (float)
  - priceChange: Thay đổi giá (float)
  - priceChangePercent: Thay đổi giá (%) (float)
  - volume: Khối lượng giao dịch (int)
  - marketCap: Vốn hóa thị trường (float)
  - pe: P/E (float)
  - pb: P/B (float)
  - eps: EPS (float)
  - dividend: Cổ tức (%) (float)
  - beta: Beta (float)
  - 52wHigh: Giá cao nhất 52 tuần (float)
  - 52wLow: Giá thấp nhất 52 tuần (float)
- **Tham số tùy chọn**:
  - exchangeName: "HOSE,HNX,UPCOM" hoặc từng sàn riêng lẻ
  - limit: Số lượng cổ phiếu tối đa (mặc định: 1700)

## 3. Advanced Functions

### 3.1 Financial Reports

#### 3.1.1 Balance Sheet
```python
balance_sheet = stock.finance.balance_sheet(
    period='year',
    lang='vi',
    dropna=True
)
```
- **Kiểu dữ liệu**: DataFrame
- **Cấu trúc**: Bảng cân đối kế toán theo năm
- **Các chỉ tiêu chính**:
  - Tài sản ngắn hạn:
    - Tiền và tương đương tiền
    - Đầu tư tài chính ngắn hạn
    - Phải thu ngắn hạn
    - Hàng tồn kho
  - Tài sản dài hạn:
    - Tài sản cố định
    - Đầu tư tài chính dài hạn
    - Tài sản dở dang dài hạn
  - Nợ phải trả:
    - Nợ ngắn hạn
    - Nợ dài hạn
  - Vốn chủ sở hữu:
    - Vốn góp
    - Lợi nhuận chưa phân phối
- **Tham số tùy chọn**:
  - period: 'year' (năm), 'quarter' (quý)
  - lang: 'vi' (tiếng Việt), 'en' (tiếng Anh)

#### 3.1.2 Income Statement
```python
income_stmt = stock.finance.income_statement(
    period='year',
    lang='vi',
    dropna=True
)
```
- **Kiểu dữ liệu**: DataFrame
- **Cấu trúc**: Báo cáo kết quả hoạt động kinh doanh
- **Các chỉ tiêu chính**:
  - Doanh thu thuần
  - Giá vốn hàng bán
  - Lợi nhuận gộp
  - Chi phí tài chính
  - Chi phí bán hàng
  - Chi phí quản lý
  - Lợi nhuận thuần
  - Lợi nhuận sau thuế
- **Tham số tùy chọn**: Tương tự Balance Sheet

#### 3.1.3 Cash Flow
```python
cash_flow = stock.finance.cash_flow(
    period='year',
    dropna=True
)
```
- **Kiểu dữ liệu**: DataFrame
- **Cấu trúc**: Báo cáo lưu chuyển tiền tệ
- **Các luồng tiền**:
  - Từ hoạt động kinh doanh:
    - Tiền thu từ bán hàng
    - Tiền chi trả nhà cung cấp
    - Tiền chi trả lương
  - Từ hoạt động đầu tư:
    - Mua sắm tài sản cố định
    - Thu từ thanh lý tài sản
  - Từ hoạt động tài chính:
    - Vay vốn
    - Trả nợ gốc
    - Chi trả cổ tức

#### 3.1.4 Financial Ratios
```python
ratios = stock.finance.ratio(
    period='year',
    lang='vi',
    dropna=True
)
```
- **Kiểu dữ liệu**: DataFrame
- **Cấu trúc**: Các chỉ số tài chính
- **Các chỉ số chính**:
  - Khả năng thanh toán:
    - Hệ số thanh toán hiện hành
    - Hệ số thanh toán nhanh
  - Hiệu quả hoạt động:
    - Vòng quay hàng tồn kho
    - Vòng quay phải thu
  - Khả năng sinh lời:
    - ROA
    - ROE
    - Biên lợi nhuận gộp
    - Biên lợi nhuận ròng
  - Đòn bẩy tài chính:
    - Hệ số nợ
    - Hệ số nợ trên vốn chủ sở hữu

### 3.2 Intraday Data
```python
intraday = stock.quote.intraday(
    symbol='ACB',
    page_size=10_000,
    show_log=False
)
```
- **Kiểu dữ liệu**: DataFrame
- **Kích thước**: (3922, 5)
- **Các cột**:
  - time: Thời gian giao dịch (datetime)
  - price: Giá giao dịch (float)
  - volume: Khối lượng giao dịch (int)
  - referencePrice: Giá tham chiếu (float)
  - priceChange: Thay đổi giá (float)
- **Tham số tùy chọn**:
  - page_size: Số lượng bản ghi tối đa (mặc định: 10,000)
  - show_log: Hiển thị log (bool)

## 4. Lưu ý khi sử dụng

1. **Xử lý dữ liệu**:
   - Sử dụng `infer_objects(copy=False)` để tránh cảnh báo về downcasting
   - Kiểm tra `None` trước khi xử lý dữ liệu
   - Cấu hình pandas:
     ```python
     pd.set_option('future.no_silent_downcasting', True)
     pd.set_option('mode.copy_on_write', True)
     ```

2. **Lỗi và ngoại lệ**:
   - Luôn sử dụng try-except khi gọi API
   - Log lỗi để dễ dàng debug
   - Kiểm tra kết quả trả về trước khi xử lý

3. **Hiệu suất**:
   - Giới hạn số lượng dữ liệu khi cần thiết
   - Sử dụng các tham số phù hợp để tối ưu hiệu suất

4. **Giới hạn API**:
   - Số lượng request tối đa: 1000 request/ngày
   - Thời gian chờ giữa các request: ít nhất 1 giây
   - Giới hạn dữ liệu lịch sử: 5 năm
   - Giới hạn dữ liệu intraday: 1 ngày

5. **Xử lý dữ liệu thiếu**:
   - Sử dụng `dropna=True` để loại bỏ dữ liệu thiếu
   - Hoặc sử dụng `fillna()` với giá trị phù hợp
   - Kiểm tra dữ liệu trước khi phân tích 