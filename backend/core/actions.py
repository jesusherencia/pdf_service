from abc import ABC, abstractmethod
from enum import Enum, auto

from core.pdf_actions import PdfActions

class ActionType(Enum):
    SHRINK = auto()
    ROTATE = auto()
    RESIZE = auto()
    @staticmethod
    def from_str(label: str):
        if label == 'SHRINK':
            return ActionType.SHRINK
        elif label == 'ROTATE':
            return ActionType.ROTATE
        elif label == 'RESIZE':
            return ActionType.RESIZE
        else:
            raise NotImplementedError

class Action(ABC):
    def __init__(self, params: dict):
        self.params = params
    
    @abstractmethod
    def execute(self, fileid: str):
        raise NotImplementedError

class ActionShrink(Action):
    """
    params :
    - img_quality : ex. [20, 50, 80] # percertange
    - dpi : ex. [150, 300]
    """
    def execute(self, fileid: str):
        call_params = {
            'fileid': fileid
        }
        if 'quality' in self.params:
            call_params['img_quality'] = self.params['quality'] # it only acts on images
        if 'dpi' in self.params:
            call_params['dpi'] = self.params['dpi']
        pdf_service = PdfActions()
        fileid_result = pdf_service.shrink2(**call_params)
        return fileid_result
        
class ActionRotate(Action):
    """
    params :
    - rotate_degree : ex. [45, 90, 180, 270]
    """
    def execute(self, fileid: str):
        rotate_degree = self.params['rotate_degree']
        pdf_service = PdfActions()
        fileid_result = pdf_service.rotate(fileid, rotate_degree)
        return fileid_result

class ActionResize(Action):
    """
    params :
    - scale : ex. [0.5, 1, 2] # multiply width and height by scale
    """
    def execute(self, fileid: str):
        scale = self.params['scale']
        pdf_service = PdfActions()
        fileid_result = pdf_service.resize_pdf(fileid, scale)
        return fileid_result

mappping_action_by_type = {
    ActionType.SHRINK: lambda params : ActionShrink(params),
    ActionType.ROTATE: lambda params : ActionRotate(params),
    ActionType.RESIZE: lambda params : ActionResize(params),
}

if __name__ == '__main__':
    #pdf_service = PdfService()
    #ActionShrink().execute("data/CBTW_attestation_pole_emploi.pdf", {'quality': 50})
    ActionRotate({'rotate_degree': 90}).execute("data/CBTW_attestation_pole_emploi.pdf")
