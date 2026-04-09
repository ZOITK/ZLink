import logging
import sys

def setup_logger(name="ZoitClient", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 이미 핸들러가 있으면 추가하지 않음 (중복 로그 방지)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# 기본 로거 인스턴스
logger = setup_logger()
