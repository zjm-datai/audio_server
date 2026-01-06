import logging
import os
import asyncio
from minio import Minio
from minio.error import S3Error
from src.config.config import Config

logger = logging.getLogger(__name__)

class OssService:

    def __init__(self, config: Config):
        self.local_folder = config.MINIO_UPLOAD_FOLDER
        self.bucket_name = config.MINIO_BUCKET_NAME
        self.path = config.MINIO_PATH

        self.minio_client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=config.MINIO_SECURE
        )

        self.create_bucket_if_not_exists(self.bucket_name)

    def create_bucket_if_not_exists(self, bucket_name):
        try:
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def _upload_file_sync(self, local_path, organize_code, conversation_id, object_name=None):
        base_file_name = os.path.basename(local_path)
        if object_name is None:
            object_name = os.path.join(organize_code, conversation_id, base_file_name)

        try:
            self.minio_client.fput_object(
                bucket_name=self.bucket_name,
                object_name=self.path + object_name,
                file_path=local_path,
            )
        except Exception as e:
            print(f"Error uploading file: {e}")
            logger.info(f"Error uploading file: {e}")
            raise

    def _download_file_sync(self, object_name):
        response = self.minio_client.get_object(
            self.bucket_name,
            self.path + object_name
        )
        try:
            content = response.read()
            local_file_path = os.path.join(self.local_folder, object_name)
            with open(local_file_path, "wb") as f:
                f.write(content)
            return local_file_path
        finally:
            response.close()
            response.release_conn()

    async def upload_file(self, local_path, organize_code, conversation_id, object_name=None):
        try:
            local_file_path = await asyncio.to_thread(
                self._upload_file_sync, local_path, organize_code, conversation_id, object_name
            )
        except S3Error:
            raise

        return local_file_path

    async def download_file(self, object_name=None):
        try:
            local_file_path =  await asyncio.to_thread(
                self._download_file_sync, object_name
            )
            return local_file_path
        except S3Error as e:
            raise
        except Exception as e:
            raise
