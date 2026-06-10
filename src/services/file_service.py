import asyncio
import logging

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import DBAPIError, InterfaceError, OperationalError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.config import Config
from src.models.file import AudioFile

logger = logging.getLogger(__name__)

DB_RETRY_ATTEMPTS = 2
DB_RETRY_DELAY_SECONDS = 0.2


class FileService:
    def __init__(self, config: Config, session_factory: async_sessionmaker[AsyncSession]):
        self.config = config
        self.session_factory = session_factory

    async def create_audio_file(
        self,
        organize_code: str,
        conversation_id: str,
        file_url: str,
        transcription_content: str = None,
    ):

        audio_file_data = {
            "organize_code": organize_code,
            "conversation_id": conversation_id,
            "file_url": file_url,
            "transcription_content": transcription_content,
        }
        audio_file_id = AudioFile(**audio_file_data).id

        for attempt in range(1, DB_RETRY_ATTEMPTS + 1):
            audio_file = AudioFile(
                id=audio_file_id,
                **audio_file_data,
            )
            try:
                async with self.session_factory() as session:
                    session.add(audio_file)
                    await session.commit()
                    await session.refresh(audio_file)
                return audio_file.id
            except SQLAlchemyError as exc:
                if not self._is_retryable_db_error(exc) or attempt == DB_RETRY_ATTEMPTS:
                    raise

                logger.warning(
                    "retrying audio file metadata insert after database connection error "
                    "(attempt %s/%s)",
                    attempt,
                    DB_RETRY_ATTEMPTS,
                    exc_info=True,
                )
                await asyncio.sleep(DB_RETRY_DELAY_SECONDS)

    @staticmethod
    def _is_retryable_db_error(exc: SQLAlchemyError) -> bool:
        if isinstance(exc, (InterfaceError, OperationalError)):
            return True
        if isinstance(exc, DBAPIError):
            return bool(exc.connection_invalidated)
        return False
