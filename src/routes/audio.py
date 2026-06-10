from typing import Annotated

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import Body, File, Depends, Form
from pydantic import BaseModel, Field
from starlette import status

from src.server.deps import get_transcription_service
from src.services.errors import FileFoundError
from src.services.transcription_service import TranscriptionService

router = APIRouter(prefix="/audio", tags=["audio"])

class TranscriptionResponse(BaseModel):
    transcription: str
    file_id: str


@router.post(
    "/transcription",
    response_model=TranscriptionResponse,
)
async def transcription(
        service: Annotated[TranscriptionService, Depends(get_transcription_service)],
        file: UploadFile = File(..., description="待转写的音频文件"),
        organize_code: str = Form(..., description="机构代码"),
        conversation_id: str | None = Form(None, description="业务对话 id"),
) -> TranscriptionResponse:
    if file.content_type != "audio/mpeg" and file.content_type != "audio/wav":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only support mp3 file")
    try:
        transcription_content, file_id = await service.get_transcription(file, organize_code, conversation_id)
    except FileFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return TranscriptionResponse(transcription=transcription_content, file_id=file_id)



