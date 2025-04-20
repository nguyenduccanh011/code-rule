# Stock Market Analysis Platform

Nền tảng phân tích thị trường chứng khoán Việt Nam, cung cấp API và giao diện người dùng để truy cập dữ liệu thị trường.

## Tài liệu

- [Tổng quan Dự án](project_overview.md) - Thông tin chi tiết về kiến trúc, công nghệ và quy trình
- [Tasks](tasks.md) - Danh sách công việc và tiến độ
- [API Documentation](backend/docs/api.md) - Tài liệu API
- [Database Schema](backend/docs/database_schema.md) - Cấu trúc cơ sở dữ liệu

## Cài đặt Nhanh

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

# Frontend
cd frontend
npm install
npm start
```

## Truy cập

- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Giấy phép

MIT 