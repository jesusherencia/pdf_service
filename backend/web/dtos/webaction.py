from pydantic import BaseModel


class WebAction(BaseModel):
    type: str
    params: dict
    """ def __init__(self, type, params):
        self.type: str = type
        self.params: dict = params """