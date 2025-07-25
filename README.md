# tntxtrick
# zLocket Tool API

API Flask được chuyển đổi từ zLocket Tool Pro - công cụ spam kết bạn và xóa yêu cầu kết bạn trên Locket.

## Tính năng

- **Spam Friend Request**: Gửi nhiều yêu cầu kết bạn đến một tài khoản Locket
- **Delete Friend Request**: Xóa hàng loạt yêu cầu kết bạn từ tài khoản của bạn
- **Multi-threading**: Hỗ trợ chạy đa luồng để tăng hiệu suất
- **Proxy Support**: Hỗ trợ sử dụng proxy để tránh bị chặn
- **CORS Enabled**: Hỗ trợ CORS cho frontend integration

## Cài đặt

### 1. Clone hoặc tải về project

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cấu hình proxy (tùy chọn)
Tạo file `proxy.txt` và thêm danh sách proxy theo định dạng:
```
192.168.1.1:8080
10.0.0.1:3128
203.0.113.1:8080
```

### 4. Chạy API
```bash
python app.py
```

API sẽ chạy trên `http://0.0.0.0:5000`

## API Endpoints

### GET /
Kiểm tra trạng thái API

### POST /spam_friend_request
Spam yêu cầu kết bạn

**Request Body:**
```json
{
    "target_url": "https://locket.cam/username",
    "custom_username": "TenCustom",
    "use_emoji": true,
    "num_threads": 10
}
```

### POST /delete_friend_request
Xóa yêu cầu kết bạn

**Request Body:**
```json
{
    "email": "your_email@example.com",
    "password": "your_password",
    "limit": 100,
    "num_threads": 5
}
```

## Testing

Chạy test suite:
```bash
python test_api.py
```

## Files

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `proxy.txt` - Proxy list (optional)
- `test_api.py` - Test suite
- `api_documentation.md` - Detailed API documentation
- `README.md` - This file

## Lưu ý

- Cần có proxy hợp lệ để spam friend request hoạt động tốt
- API được thiết kế để chạy trên server
- Hỗ trợ CORS cho tất cả origins
- Tất cả endpoints sử dụng JSON format

## Bảo mật

- Không lưu trữ thông tin đăng nhập
- Sử dụng HTTPS khi deploy production
- Giới hạn rate limiting nếu cần thiết

## License

Dựa trên zLocket Tool Pro by @WsThanhDieu
[ Uống nước nhớ nguồn😏 ]

