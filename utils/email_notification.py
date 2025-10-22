import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile
from datetime import datetime

# Cấu hình
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'cuasophongem69@gmail.com'
RECEIVER_EMAIL = 'cheese12804@gmail.com'
APP_PASSWORD = 'bhnt tyyz fgvs xjqc'
JENKINS_URL = 'http://localhost:8080/job/Saudemo/allure/'
JENKINS_JOB_NAME = 'test-automation'


def create_zip(source_dir, zip_path):
    """Tạo zip file"""
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        return True
    except:
        return False


def get_jenkins_link():
    """Lấy Jenkins link"""
    try:
        build_number = os.getenv('BUILD_NUMBER', 'lastSuccessfulBuild')
        if build_number == 'lastSuccessfulBuild':
            return f"{JENKINS_URL}"
        else:
            return f"{JENKINS_URL}"
    except:
        return None


def send_allure_report_email(allure_results_dir, test_summary=None):
    """Gửi email với Jenkins link"""
    try:
        # Lấy Jenkins link
        jenkins_url = get_jenkins_link()
        
        # Tạo zip
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"allure_report_{timestamp}.zip"
        zip_path = os.path.join(os.path.dirname(allure_results_dir), zip_filename)
        
        if not create_zip(allure_results_dir, zip_path):
            return False
        
        # Tạo email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Nội dung email
        test_info = ""
        if test_summary:
            for key, value in test_summary.items():
                test_info += f"{key}: {value}\n"
        
        body = f"""Test execution completed.

Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Results Directory: {allure_results_dir}

Test Summary:
{test_info}

Report Link: {jenkins_url if jenkins_url else 'Not available'}

Attachment: {zip_filename}
To view: Extract zip file and open index.html in browser"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Đính kèm zip
        if os.path.exists(zip_path):
            with open(zip_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {zip_filename}')
                msg.attach(part)
        
        # Gửi email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print(f"Email sent to {RECEIVER_EMAIL}")
        if jenkins_url:
            print(f"Report link: {jenkins_url}")
        
        # Xóa zip
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_simple_notification(allure_results_dir):
    """Gửi thông báo đơn giản"""
    try:
        jenkins_url = get_jenkins_link()
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Test Completed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""Test execution completed.

Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Results Directory: {allure_results_dir}

Report Link: {jenkins_url if jenkins_url else 'Not available'}"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print(f"Simple notification sent to {RECEIVER_EMAIL}")
        if jenkins_url:
            print(f"Report link: {jenkins_url}")
        return True
        
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False
