from typing import Annotated

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.config import Config
from src.server.db import get_session
from src.services.audio_service import AudioService
from src.services.file_service import FileService
from src.services.local_service import LocalService
from src.services.oss_service import OssService
from src.services.transcription_service import TranscriptionService


def get_config() -> Config:
    return Config()

def get_oss_service(
        config: Annotated[Config, Depends(get_config)]
):
    return OssService(config)

def get_file_service(
        config: Annotated[Config, Depends(get_config)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    return FileService(config, session)

def get_audio_service(
        config: Annotated[Config, Depends(get_config)]
):
    return AudioService(config)

def get_local_service(
        config: Annotated[Config, Depends(get_config)]
) -> LocalService:
    return LocalService(config)

def get_transcription_service(
        config: Annotated[Config, Depends(get_local_service)],
        file_service: Annotated[FileService, Depends(get_file_service)],
        audio_service: Annotated[AudioService, Depends(get_audio_service)],
        oss_service: Annotated[OssService, Depends(get_oss_service)],
        local_service: Annotated[LocalService, Depends(get_local_service)],
) -> TranscriptionService:
    return TranscriptionService(
        config=config,
        file_service=file_service,
        audio_service=audio_service,
        oss_service=oss_service,
        local_service=local_service,
    )