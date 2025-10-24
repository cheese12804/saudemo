import logging
import os
def setup_logger():
    # Tạo logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))

    # Tạo đường dẫn cho thư mục logs và file log
    log_dir = os.path.join(project_root, 'logs')
    log_file_path = os.path.join(log_dir, 'test_log.txt')

    # Tạo thư mục logs nếu chưa tồn tại
    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()
