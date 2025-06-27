from abc import ABC, abstractmethod
from enum import Enum, auto

from core.pdf_actions import PdfActions

class ActionType(Enum):
    SHRINK = auto()
    ROTATE = auto()
    @staticmethod
    def from_str(label: str):
        if label == 'SHRINK':
            return ActionType.SHRINK
        elif label == 'ROTATE':
            return ActionType.ROTATE
        else:
            raise NotImplementedError

class ActionTypeParams():
    def __init__(self, type, params):
        self.type: ActionType = type
        self.params: dict = params

class Action(ABC):
    @abstractmethod
    def execute(self, fileid: str, params: dict):
        raise NotImplementedError

class ActionShrink(Action):
    def execute(self, fileid: str, params: dict):
        quality = params['quality']
        pdf_service = PdfActions()
        fileid_result = pdf_service.shrink(fileid, quality)
        return fileid_result
        
class ActionRotate(Action):
    def execute(self, fileid: str, params: dict):
        rotate_degree = params['rotate_degree']
        pdf_service = PdfActions()
        fileid_result = pdf_service.rotate(fileid, rotate_degree)
        return fileid_result

mappping_type_actionclass = {
    ActionType.SHRINK: ActionShrink(),
    ActionType.ROTATE: ActionRotate(),
}

if __name__ == '__main__':
    #pdf_service = PdfService()
    #ActionShrink().execute("data/CBTW_attestation_pole_emploi.pdf", {'quality': 50})
    ActionRotate().execute("data/CBTW_attestation_pole_emploi.pdf", {'rotate_degree': 90})
