from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class AudioFile(SQLModel, table=True):

    __tablename__ = "audio_file"

    id: int = Field(default=None, primary_key=True, index=True)

    organize_code: int = Field(index=True)
    conversation_id: int = Field(index=True)
    file_url: str = Field()
    transcription_content: str = Field()

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None),
        index=True
    )