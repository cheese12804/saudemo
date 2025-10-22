#!/usr/bin/env python3
"""
Script test email notification
Chạy script này để kiểm tra xem email notification có hoạt động không
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Thêm project root vào Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from utils.email_notification import send_email_with_attachment, send_simple_notification

def create_test_allure_results():
    """Tạo thư mục allure-results test với một số file mẫu"""
    # Tạo thư mục tạm thời
    temp_dir = tempfile.mkdtemp(prefix="test_allure_")
    allure_dir = os.path.join(temp_dir, "allure-results")
    os.makedirs(allure_dir, exist_ok=True)
    
    # Tạo một số file mẫu
    test_files = [
        "environment.properties",
        "test_result.json",
        "screenshot.png"
    ]
    
    for filename in test_files:
        file_path = os.path.join(allure_dir, filename)
        with open(file_path, 'w') as f:
            if filename == "environment.properties":
                f.write("os=Windows 10\nbrowser=Chrome\npython_version=3.9.0\n")
            elif filename == "test_result.json":
                f.write('{"test_name": "test_example", "status": "passed"}\n')
            else:
                f.write("fake screenshot content\n")
    
    print(f"Created test allure results at: {allure_dir}")
    return allure_dir

def test_email_with_attachment():
    """Test gửi email với file đính kèm"""
    print("\n=== Testing Email with Attachment ===")
    
    # Tạo test data
    allure_dir = create_test_allure_results()
    test_summary = {
        "Total Tests": 5,
        "Passed": 4,
        "Failed": 1,
        "Exit Status": 1
    }
    
    try:
        success = send_email_with_attachment(allure_dir, test_summary)
        if success:
            print("✅ Email with attachment sent successfully!")
        else:
            print("❌ Failed to send email with attachment")
        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Cleanup
        shutil.rmtree(os.path.dirname(allure_dir), ignore_errors=True)

def test_simple_notification():
    """Test gửi thông báo đơn giản"""
    print("\n=== Testing Simple Notification ===")
    
    allure_dir = create_test_allure_results()
    
    try:
        success = send_simple_notification(allure_dir)
        if success:
            print("✅ Simple notification sent successfully!")
        else:
            print("❌ Failed to send simple notification")
        return success
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Cleanup
        shutil.rmtree(os.path.dirname(allure_dir), ignore_errors=True)

def main():
    """Main function để test email notification"""
    print("🧪 Testing Email Notification System")
    print("=" * 50)
    
    # Kiểm tra cấu hình email
    try:
        from configs.email_config import SENDER_EMAIL, RECEIVER_EMAIL, PASSWORD
        print(f"📧 Sender: {SENDER_EMAIL}")
        print(f"📧 Receiver: {RECEIVER_EMAIL}")
        print(f"🔑 Password: {'*' * len(PASSWORD) if PASSWORD != 'your_email_password' else 'NOT SET'}")
        
        if PASSWORD == 'your_email_password':
            print("⚠️  WARNING: Please update your email password in configs/email_config.py")
            print("   For Gmail, use App Password if 2FA is enabled")
            return
        
    except ImportError as e:
        print(f"❌ Error importing email config: {e}")
        return
    
    # Test email với attachment
    attachment_success = test_email_with_attachment()
    
    # Test simple notification
    simple_success = test_simple_notification()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Email with Attachment: {'✅ PASS' if attachment_success else '❌ FAIL'}")
    print(f"   Simple Notification: {'✅ PASS' if simple_success else '❌ FAIL'}")
    
    if attachment_success or simple_success:
        print("\n🎉 Email notification system is working!")
    else:
        print("\n💥 Email notification system failed!")
        print("   Please check your email configuration and credentials")

if __name__ == "__main__":
    main()
