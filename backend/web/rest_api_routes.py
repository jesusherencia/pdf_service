from io import BytesIO
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from core.actions import ActionType, ActionTypeParams
from core.file_repository import FileRepository
from core.pdf_edit_service import PdfEditService
from typing import List

from shared.logger import Logger
from web.dtos.file_webactions import FileWebActions
from web.dtos.merge_pdf_files import MergePdfFiles
from web.dtos.stocked_file import StockedFile

router = APIRouter(prefix='/api')

logger = Logger.get_current_logger()

@router.post("/pdf_file/upload")
async def create_upload_file(file: UploadFile) -> StockedFile:
    content = await file.read()
    file_id = PdfEditService().save_pdf_file(content)
    logger.info("File uploaded id : " + file_id)
    return StockedFile(file_id=file_id)

@router.get("/pdf_file/{file_id}")
async def get_file(file_id: str):
    content = FileRepository().get(file_id) # use PdfEditService instead
    file_like = BytesIO(content)
    # Return as a downloadable file
    return StreamingResponse(
        file_like,
        media_type="application/pdf",  # Change to appropriate media type if needed
        headers={
            "Content-Disposition": f'attachment; filename="{file_id}.pdf"'
        }
    )

@router.post("/pdf_file/webactions")
async def execute_actions(file_webactions: FileWebActions):
    print(file_webactions)
    actions: List[ActionType] = []
    for i in file_webactions.webactions:
        actions.append(ActionTypeParams(ActionType.from_str(i.type), i.params))
    file_id = PdfEditService().execute_actions(file_webactions.file_id, actions)
    return StockedFile(file_id=file_id)

@router.post("/pdf_file/merge")
async def merge_pdfs(merge_pdf_files: MergePdfFiles):
    file_id = PdfEditService().merge_pdf_files(merge_pdf_files.fileid_list)
    return StockedFile(file_id=file_id)