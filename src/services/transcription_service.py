from fastapi import UploadFile

from src.config.config import Config
from src.services.audio_service import AudioService
from src.services.errors import FileFoundError
from src.services.file_service import FileService
from src.services.local_service import LocalService
from src.services.oss_service import OssService


class TranscriptionService:
    def __init__(
            self,
            config: Config = None,
            file_service: FileService = None,
            audio_service: AudioService = None,
            oss_service: OssService = None,
            local_service: LocalService = None,
    ):
        self.config = config
        self.file_service = file_service
        self.audio_service = audio_service
        self.oss_service = oss_service
        self.local_service = local_service

    async def get_transcription(
            self, file: UploadFile, organize_code: str, conversation_id: str,
    )-> tuple[str, str]:
        try:
            local_path = await self.local_service.save_file(file, organize_code, conversation_id)

            await self.oss_service.upload_file(local_path, organize_code, conversation_id)

            audio_file_url = f"{self.config.FILE_DOWNLOAD_URL}/file/{organize_code}-{conversation_id}/{file.filename}"
            transcription_content = await self.audio_service.transcribe(audio_file_url)

            file_id = await self.file_service.create_audio_file(
                organize_code=organize_code,
                conversation_id=conversation_id,
                file_url=audio_file_url,
                transcription_content=transcription_content,
            )
            return transcription_content, file_id
        except FileFoundError:
            raise
        except Exception as e:
            raise

