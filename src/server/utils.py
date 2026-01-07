import os 
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from zoneinfo import ZoneInfo
from datetime import datetime

from src.config import Config

class FixedTimezoneFormatter(logging.Formatter):
    
    def __init__(self, *args, tz: ZoneInfo, **kwargs):
        super().__init__(*args, **kwargs)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created).astimezone(self.tz)
        return dt.isoformat(timespec="seconds")

def setup_logging(config: Config):
    
    formatter = FixedTimezoneFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        tz=config.get_zoneinfo()
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    handlers = [console_handler]
    
    if config.TO_FILE:
        os.makedirs(config.LOG_DIR, exist_ok=True)
        log_path = os.path.join(config.LOG_DIR, config.LOG_FILENAME)

        file_handler = TimedRotatingFileHandler(
            filename=log_path,
            when=config.ROTATE_WHEN,
            interval=config.ROTATE_INTERVAL,
            backupCount=config.ROTATE_BACKUP_COUNT,
            encoding="utf-8",
            utc=False  # 我们自己处理时区
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # 设置 root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if config.DEBUG else config.get_log_level())
    root_logger.handlers.clear()
    for handler in handlers:
        root_logger.addHandler(handler)

    # 输出一条初始化成功日志
    logging.getLogger(__name__).info(
        "Logging initialized | level=%s | file=%s | tz=%s",
        config.LOG_LEVEL,
        os.path.join(config.LOG_DIR, config.LOG_FILENAME) if config.TO_FILE else "N/A",
        config.TIMEZONE,
    )