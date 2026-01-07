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
            logger.error(f"Error creating bucket: {e}")

    def _upload_file_sync(self, local_path, organize_code, conversation_id, object_name=None):
        base_file_name = os.path.basename(local_path)
        if object_name is None:
            object_name = os.path.join(organize_code, conversation_id, base_file_name)
        
        try:
            # 上传文件并返回对象名称（原代码无返回值，补充返回便于后续使用）
            self.minio_client.fput_object(
                bucket_name=self.bucket_name,
                object_name=self.path + '/' + object_name,
                file_path=local_path,
            )
            return self.path + '/' + object_name  # 返回完整的对象路径
        except Exception as e:
            print(f"Error uploading file: {e}")
            logger.error(f"Error uploading file: {e}")  # 改为error级别日志
            raise

    def _download_file_sync(self, object_name):

        full_object_name = self.path + '/' + object_name
        
        logger.info(f"full_object_name is {full_object_name}")
        
        response = self.minio_client.get_object(
            self.bucket_name,
            full_object_name
        )
        
        try:
            content = response.read()
            # 确保本地文件夹存在
            local_file_dir = os.path.dirname(os.path.join(self.local_folder, object_name))
            os.makedirs(local_file_dir, exist_ok=True)
            
            local_file_path = os.path.join(self.local_folder, object_name)
            with open(local_file_path, "wb") as f:
                f.write(content)
            return local_file_path
        finally:
            response.close()
            response.release_conn()

    async def upload_file(self, local_path, organize_code, conversation_id, object_name=None):

        try:
            # 验证本地文件是否存在
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"Local file not found: {local_path}")
            
            object_path = await asyncio.to_thread(
                self._upload_file_sync,
                local_path,
                organize_code,
                conversation_id,
                object_name
            )
            logger.info(f"File uploaded successfully: {local_path} -> {object_path}")
            return object_path
        except S3Error as e:
            logger.error(f"S3 error when uploading file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when uploading file: {e}")
            raise

    async def download_file(self, object_name):
        if not object_name:
            raise ValueError("object_name cannot be empty")
        
        try:
            local_file_path = await asyncio.to_thread(
                self._download_file_sync,
                object_name
            )
            logger.info(f"File downloaded successfully: {object_name} -> {local_file_path}")
            return local_file_path
        except S3Error as e:
            logger.error(f"S3 error when downloading file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when downloading file: {e}")
            raise