# Hướng dẫn thiết lập Email Notification

## Tổng quan
Hệ thống email notification sẽ tự động gửi kết quả test (Allure results) qua email sau khi chạy pytest.

## Cấu hình Email

### 1. Cập nhật thông tin email
Chỉnh sửa file `configs/email_config.py`:

```python
# Email Credentials
SENDER_EMAIL = 'your_email@gmail.com'  # Email gửi
RECEIVER_EMAIL = 'recipient@gmail.com'  # Email nhận
PASSWORD = 'your_app_password'  # Mật khẩu hoặc App Password
```

### 2. Cấu hình Gmail (nếu sử dụng Gmail)

#### Bước 1: Bật 2-Factor Authentication
1. Vào Google Account Settings
2. Security → 2-Step Verification
3. Bật 2-Step Verification

#### Bước 2: Tạo App Password
1. Vào Google Account Settings
2. Security → 2-Step Verification → App passwords
3. Chọn "Mail" và "Other (Custom name)"
4. Nhập tên: "Test Automation"
5. Copy App Password (16 ký tự)
6. Dán vào `PASSWORD` trong `email_config.py`

### 3. Cấu hình khác
```python
# Email Settings
ENABLE_EMAIL_NOTIFICATION = True  # Bật/tắt gửi email
SEND_ATTACHMENT = True  # Gửi file zip đính kèm
SEND_SIMPLE_NOTIFICATION = True  # Gửi thông báo đơn giản nếu không gửi được attachment
```

## Cách sử dụng

### 1. Chạy test với email notification
```bash
# Chạy test bình thường - email sẽ tự động gửi
pytest tests/test_buy_product.py -v --alluredir=allure-results

# Hoặc chạy tất cả test
pytest --alluredir=allure-results
```

### 2. Test email notification riêng
```bash
# Chạy script test email
python test_email_notification.py
```

### 3. Tắt email notification
Chỉnh sửa `configs/email_config.py`:
```python
ENABLE_EMAIL_NOTIFICATION = False
```

## Tính năng

### 1. Email với file đính kèm
- Tự động tạo file zip chứa toàn bộ allure-results
- Gửi email với file zip đính kèm
- Tự động xóa file zip tạm thời sau khi gửi

### 2. Email thông báo đơn giản
- Gửi thông báo text đơn giản nếu không gửi được file đính kèm
- Chứa thông tin về thời gian chạy test và kết quả

### 3. Template email
- Email HTML với thông tin chi tiết
- Test summary với số liệu thống kê
- Hướng dẫn xem report

## Troubleshooting

### 1. Lỗi "Authentication failed"
- Kiểm tra email và password
- Đảm bảo sử dụng App Password cho Gmail
- Kiểm tra 2FA đã được bật

### 2. Lỗi "Connection refused"
- Kiểm tra kết nối internet
- Kiểm tra firewall/antivirus
- Thử đổi SMTP port (587 thay vì 465)

### 3. Không nhận được email
- Kiểm tra spam folder
- Kiểm tra email address đúng
- Kiểm tra logs trong console

### 4. File zip quá lớn
- Gmail giới hạn 25MB
- Có thể giảm kích thước bằng cách chỉ gửi file quan trọng
- Hoặc upload lên cloud storage và gửi link

## Logs và Debug

### 1. Xem logs trong console
```
[Email Notification] Sending test results via email...
[Email Notification] Allure results directory: /path/to/allure-results
[Email Notification] Email with attachment sent successfully!
```

### 2. Debug email config
```python
# Thêm vào conftest.py để debug
print(f"Email config: {SENDER_EMAIL} -> {RECEIVER_EMAIL}")
```

## Cấu trúc file

```
project/
├── configs/
│   └── email_config.py          # Cấu hình email
├── utils/
│   └── email_notification.py    # Logic gửi email
├── conftest.py                  # Pytest hooks
├── test_email_notification.py   # Script test email
└── EMAIL_SETUP_GUIDE.md         # Hướng dẫn này
```

## Lưu ý bảo mật

1. **Không commit password vào git**
   - Thêm `configs/email_config.py` vào `.gitignore`
   - Sử dụng environment variables cho production

2. **Sử dụng App Password**
   - Không sử dụng password chính của Gmail
   - Tạo App Password riêng cho automation

3. **Giới hạn quyền truy cập**
   - Chỉ gửi email nội bộ
   - Không gửi thông tin nhạy cảm
