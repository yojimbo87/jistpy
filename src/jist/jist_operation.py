from typing import Generic, TypeVar
from pydantic import BaseModel, Field

ContentT = TypeVar("ContentT")


class JistError(BaseModel):
    code: int
    row_id: int = Field(alias="rowId")
    message: str
    localized_message: str = Field(alias="localizedMessage")


class JistOperation(Generic[ContentT]):
    def __init__(self, status_code: int):
        self.status_code = status_code
        self.content: ContentT = None
        self.error: JistError = None

    @property
    def is_success(self):
        return (
            True
            if (self.error is None) and (self.content is not None)
            else False
        )
