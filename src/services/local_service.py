import os
import logging
from fastapi import UploadFile

from src.config.config import Config
from src.services.errors import FileFoundError

logger = logging.getLogger(__name__)

class LocalService:

    def __init__(self, config: Config):
        self.config = config
        self.upload_folder = config.MINIO_UPLOAD_FOLDER
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    async def save_file(self, file: UploadFile, organize_code: str, conversation_id: str):
        target_dir = os.path.join(self.upload_folder, organize_code, conversation_id)
        file_path = os.path.join(target_dir, file.filename)
        if os.path.exists(file_path):
            raise FileFoundError

        os.makedirs(target_dir, exist_ok=True)

        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)

        return file_path

    def get_file_path(self, organize_code: str, conversation_id: str, filename: str):
        return os.path.join(self.upload_folder, organize_code, conversation_id, filename)
