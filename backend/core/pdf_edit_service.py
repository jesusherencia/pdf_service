from core.file_repository import FileRepository
from core.actions import Action
from typing import List

from core.pdf_actions import PdfActions


class PdfEditService():
    """
    Facade service
    """

    def save_pdf_file(self, file_content):
        """
        Store file by using FileService and returning a fileid
        """
        fileid = FileRepository().put(file_content)
        return fileid
    
    def execute_actions(self, fileid, actions: List[Action]):
        """
        Execute actions over file identified by fileid
        """
        for action in actions:
            fileid = action.execute(fileid)
        return fileid
    
    def merge_pdf_files(self, fileid_list: List[str]):
        return PdfActions().merge_pdf_files(fileid_list)