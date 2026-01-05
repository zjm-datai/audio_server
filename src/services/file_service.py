
from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.config import Config
from src.models.file import AudioFile


class FileService:
    def __init__(self, config: Config, session: AsyncSession):
        self.config = config
        self.session = session

    async def create_audio_file(
        self,
        organize_code: str,
        conversation_id: str,
        file_url: str,
        transcription_content: str = None,
    ):

        audio_file = AudioFile(
            organize_code=organize_code,
            conversation_id=conversation_id,
            file_url=file_url,
            transcription_content=transcription_content,
        )
        self.session.add(audio_file)
        try:
            await self.session.commit()
            await self.session.refresh(audio_file)
            return audio_file.id
        except SQLAlchemyError:
            await self.session.rollback()
            raise
