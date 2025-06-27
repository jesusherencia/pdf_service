from core.file_repository import FileRepository
from core.actions import Action, ActionTypeParams, mappping_type_actionclass
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
    
    def execute_actions(self, fileid, actions_type_params: List[ActionTypeParams]):
        """
        Execute actions over file identified by fileid
        """
        for i in actions_type_params:
            action: Action = mappping_type_actionclass[i.type]
            fileid = action.execute(fileid, i.params)
        return fileid
    
    def merge_pdf_files(self, fileid_list: List[str]):
        return PdfActions().merge_pdf_files(fileid_list)