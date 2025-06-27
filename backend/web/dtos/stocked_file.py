from pydantic import BaseModel


class StockedFile(BaseModel):
    file_id: str