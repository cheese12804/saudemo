import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
import zipfile
from datetime import datetime

# Import email configuration
try:
    from configs.email_config import (
        SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, RECEIVER_EMAIL, PASSWORD,
        ENABLE_EMAIL_NOTIFICATION, SEND_ATTACHMENT, SEND_SIMPLE_NOTIFICATION,
        EMAIL_SUBJECT_PREFIX, EMAIL_BODY_TEMPLATE
    )
except ImportError:
    # Fallback configuration
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    SENDER_EMAIL = 'cuasophongem69@gmail.com'
    RECEIVER_EMAIL = 'cheese12804@gmail.com'
    PASSWORD = 'your_email_password'
    ENABLE_EMAIL_NOTIFICATION = True
    SEND_ATTACHMENT = True
    SEND_SIMPLE_NOTIFICATION = True
    EMAIL_SUBJECT_PREFIX = "Test Results"
    EMAIL_BODY_TEMPLATE = "Test execution completed. Please check the results."


def create_zip_file(source_dir, zip_path):
    """Tạo file zip từ thư mục allure-results"""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        print(f"Created zip file: {zip_path}")
        return True
    except Exception as e:
        print(f"Error creating zip file: {e}")
        return False


def send_email_with_attachment(allure_results_dir, test_summary=None):
    """Gửi email với file zip chứa allure results"""
    try:
        # Tạo file zip
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"allure_results_{timestamp}.zip"
        zip_path = os.path.join(os.path.dirname(allure_results_dir), zip_filename)
        
        if not create_zip_file(allure_results_dir, zip_path):
            return False
        
        # Tạo email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Tạo test summary HTML
        test_summary_html = ""
        if test_summary:
            for key, value in test_summary.items():
                test_summary_html += f"<li><strong>{key}:</strong> {value}</li>"
        
        # Nội dung email sử dụng template
        body = EMAIL_BODY_TEMPLATE.format(
            execution_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            results_dir=allure_results_dir,
            test_summary=test_summary_html
        )
        
        msg.attach(MIMEText(body, 'html'))
        
        # Đính kèm file zip
        if os.path.exists(zip_path):
            with open(zip_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {zip_filename}',
                )
                msg.attach(part)
        
        # Gửi email
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        
        print(f"Email sent successfully to {RECEIVER_EMAIL}")
        
        # Xóa file zip tạm thời
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"Temporary zip file removed: {zip_path}")
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_simple_notification(allure_results_dir):
    """Gửi thông báo đơn giản không có file đính kèm"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
        Test execution has been completed.
        
        Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Results Directory: {allure_results_dir}
        
        Please check the Allure results directory for detailed reports.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        
        print(f"Notification email sent to {RECEIVER_EMAIL}")
        return True
        
    except Exception as e:
        print(f"Error sending notification email: {e}")
        return False
