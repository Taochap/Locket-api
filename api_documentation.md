# zLocket Tool API Documentation

## Mô tả
API Flask được chuyển đổi từ zLocket Tool Pro - công cụ spam kết bạn và xóa yêu cầu kết bạn trên Locket.

## Endpoints

### 1. GET /
**Mô tả:** Kiểm tra trạng thái API
**Response:**
```
zLocket API is running!
```

### 2. POST /spam_friend_request
**Mô tả:** Spam yêu cầu kết bạn đến một tài khoản Locket

**Request Body:**
```json
{
    "target_url": "https://locket.cam/username_hoac_link",
    "custom_username": "TenCustom",
    "use_emoji": true,
    "num_threads": 10
}
```

**Parameters:**
- `target_url` (required): Link Locket hoặc username của mục tiêu
- `custom_username` (optional): Tên hiển thị tùy chỉnh (mặc định: "zLocket Tool Pro")
- `use_emoji` (optional): Sử dụng emoji ngẫu nhiên (mặc định: true)
- `num_threads` (optional): Số luồng chạy song song (mặc định: 1)

**Response Success:**
```json
{
    "status": "success",
    "message": "Friend request spamming initiated."
}
```

**Response Error:**
```json
{
    "status": "error",
    "message": "Error description"
}
```

### 3. POST /delete_friend_request
**Mô tả:** Xóa yêu cầu kết bạn từ tài khoản Locket

**Request Body:**
```json
{
    "email": "your_email@example.com",
    "password": "your_password",
    "limit": 100,
    "num_threads": 5
}
```

**Parameters:**
- `email` (required): Email tài khoản Locket
- `password` (required): Mật khẩu tài khoản Locket
- `limit` (optional): Số lượng yêu cầu muốn xóa (mặc định: tất cả)
- `num_threads` (optional): Số luồng chạy song song (mặc định: 1)

**Response Success:**
```json
{
    "status": "success",
    "message": "Successfully deleted X friend requests."
}
```

**Response Error:**
```json
{
    "status": "error",
    "message": "Error description"
}
```

## Cài đặt và Chạy

### 1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

### 2. Tạo file proxy.txt (tùy chọn):
Thêm danh sách proxy theo định dạng IP:PORT, mỗi proxy một dòng.

### 3. Chạy API:
```bash
python app.py
```

API sẽ chạy trên `http://0.0.0.0:5000`

## Lưu ý
- Cần có file `proxy.txt` với danh sách proxy hợp lệ để spam friend request hoạt động
- API hỗ trợ CORS cho tất cả origins
- Tất cả endpoints đều hỗ trợ JSON request/response
- API được thiết kế để chạy trên server với khả năng truy cập từ bên ngoài

## Ví dụ sử dụng

### Spam friend request:
```bash
curl -X POST http://localhost:5000/spam_friend_request \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://locket.cam/example_user",
    "custom_username": "MyBot",
    "use_emoji": true,
    "num_threads": 5
  }'
```

### Xóa friend request:
```bash
curl -X POST http://localhost:5000/delete_friend_request \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your_email@example.com",
    "password": "your_password",
    "limit": 50,
    "num_threads": 3
  }'
```

