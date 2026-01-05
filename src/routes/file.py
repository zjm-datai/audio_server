import os
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse
from starlette import status

from src.services.local_service import LocalService
from src.services.oss_service import OssService
from src.server.deps import get_local_service, get_oss_service

router = APIRouter(prefix="/file", tags=["file"])

@router.get("/{organize_code}-{conversation_id}/{filename}")
async def get_file(
        organize_code: str,
        conversation_id: str,
        filename: str,
        local_service: Annotated[LocalService, Depends(get_local_service)],
        oss_service: Annotated[OssService, Depends(get_oss_service)],
):
    local_path = local_service.get_file_path(filename, organize_code, conversation_id)
    if os.path.exists(local_path):
        return FileResponse(local_path, filename=filename)

    try:
        local_file_path = await oss_service.download_file(filename)
        return FileResponse(local_file_path, filename=filename)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))