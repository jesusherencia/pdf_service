from typing import List

from pydantic import BaseModel

from core.actions import Action
from web.dtos.webaction import WebAction

class FileWebActions(BaseModel):
    
    file_id: str
    webactions: List[WebAction]

    """ def __init__(self, file_id: str, webactions: List[WebAction]):
        file_id: str = file_id
        webactions: List[WebAction] = webactions """

    def to_actions(self) -> List[Action]:
        return [wa.to_action() for wa in self.webactions]