
from typing import List

from zoneinfo import ZoneInfo
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool
    MINIO_UPLOAD_FOLDER: str
    MINIO_BUCKET_NAME: str
    MINIO_PATH: str

    STT_API_KEY: str
    STT_MODEL: str
    STT_API_URL: str

    DATABASE_URL: str

    ENABLE_CORS: bool
    ALLOW_ORIGINS: str
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: str
    ALLOW_HEADERS: str

    FILE_DOWNLOAD_URL: str
    
    DEBUG: bool
    TO_FILE: bool
    LOG_DIR: str 
    LOG_FILENAME: str
    LOG_LEVEL: str 
    TIMEZONE: str 
    ROTATE_WHEN: str
    ROTATE_INTERVAL: int 
    ROTATE_BACKUP_COUNT: int 
    
    def get_zoneinfo(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE)

    def get_log_level(self) -> int:
        import logging
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)
    

    model_config = SettingsConfigDict(
        env_prefix="AS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )