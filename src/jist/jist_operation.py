from typing import Generic, TypeVar
from pydantic import BaseModel, Field

ContentT = TypeVar("ContentT")


class JistError(BaseModel):
    code: int = Field(default=None)
    row_id: int = Field(default=None, alias="rowId")
    message: str
    localized_message: str = Field(default=None, alias="localizedMessage")
    # Used only by Jira REST API, e.g. during token request
    status_code: int = Field(default=None, alias="status-code")
    # Used only by Jira REST API, e.g. during token request
    sub_code: int = Field(default=None, alias="sub-code")


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
