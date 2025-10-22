# Email Configuration
# Cấu hình thông tin email để gửi kết quả test

# SMTP Server Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # SSL port

# Email Credentials
SENDER_EMAIL = 'cuasophongem69@gmail.com'
RECEIVER_EMAIL = 'cheese12804@gmail.com'
PASSWORD = 'your_email_password'  # Thay bằng mật khẩu thực tế hoặc App Password

# Email Settings
ENABLE_EMAIL_NOTIFICATION = True  # Bật/tắt gửi email
SEND_ATTACHMENT = True  # Gửi file zip đính kèm
SEND_SIMPLE_NOTIFICATION = True  # Gửi thông báo đơn giản nếu không gửi được attachment

# Email Content
EMAIL_SUBJECT_PREFIX = "Test Results"
EMAIL_BODY_TEMPLATE = """
<h2>Test Execution Completed</h2>
<p><strong>Execution Time:</strong> {execution_time}</p>
<p><strong>Results Directory:</strong> {results_dir}</p>
<p><strong>Test Summary:</strong></p>
<ul>
{test_summary}
</ul>
<p>Please find the attached Allure results in the zip file.</p>
<p>To view the report, extract the zip file and open index.html in a web browser.</p>
"""
