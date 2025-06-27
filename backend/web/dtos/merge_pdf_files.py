from typing import List
from pydantic import BaseModel


class MergePdfFiles(BaseModel):
    fileid_list: List