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

    ENABLE_CORS: str
    ALLOW_ORIGINS: str
    ALLOW_CREDENTIALS: str
    ALLOW_METHODS: str
    ALLOW_HEADERS: str

    FILE_DOWNLOAD_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )