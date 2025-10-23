import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile
from datetime import datetime

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'cuasophongem69@gmail.com'
RECEIVER_EMAIL = 'cheese12804@gmail.com'
APP_PASSWORD = 'bhnt tyyz fgvs xjqc'


def create_zip(source_dir, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
 


def send_test_results_email(allure_results_dir=None):
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    build_number = os.getenv('BUILD_NUMBER', 'Unknown')
    job_link = f"http://localhost:8080/job/Saudemo/{build_number}/allure/" if build_number != 'Unknown' else "http://localhost:8080/job/Saudemo/"
    
    passed = 0
    failed = 0
    
    if allure_results_dir and os.path.exists(allure_results_dir):
        # Đếm từ allure results files
        for file in os.listdir(allure_results_dir):
            if file.endswith('.json'):
                file_path = os.path.join(allure_results_dir, file)
                try:
                    import json
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('status') == 'passed':
                            passed += 1
                        elif data.get('status') == 'failed':
                            failed += 1
                except:
                    continue
    
    # Tạo email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"Test Results - {execution_time}"
    
    body = f"""1. Execution time: {execution_time}
2. Build number: {build_number}
3. Passed: {passed}
4. Failed: {failed}
5. Job link: {job_link}
6. Allure file: {'Attached' if allure_results_dir else 'Not available'}"""

    msg.attach(MIMEText(body, 'plain'))
    
    # Đính kèm Allure file nếu có
    if allure_results_dir and os.path.exists(allure_results_dir):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"allure_report_{timestamp}.zip"
        zip_path = os.path.join(os.path.dirname(allure_results_dir), zip_filename)
        
        if create_zip(allure_results_dir, zip_path) and os.path.exists(zip_path):
            with open(zip_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {zip_filename}')
                msg.attach(part)
            
            # Xóa zip sau khi đính kèm
            os.remove(zip_path)
    
    # Gửi email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    
    print(f"Email sent to {RECEIVER_EMAIL}")
    print(f"Job link: {job_link}")


