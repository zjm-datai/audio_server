from uuid import uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class AudioFile(SQLModel, table=True):

    __tablename__ = "audio_file"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)

    organize_code: str = Field(index=True)
    conversation_id: str = Field(index=True)
    file_url: str = Field()
    transcription_content: str = Field()

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None),
        index=True
    )