from pydantic import BaseModel

from core.actions import Action, ActionType, mappping_action_by_type


class WebAction(BaseModel):
    type: str
    params: dict
    """ def __init__(self, type, params):
        self.type: str = type
        self.params: dict = params """
    
    def to_action(self) -> Action:
        return mappping_action_by_type[ActionType.from_str(self.type)](self.params)