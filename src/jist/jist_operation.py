from typing import Generic, TypeVar
from requests import Response
from pydantic import Field

ContentT = TypeVar("ContentT")

# {"code":4800,
# "error":"SUBSCRIPTION_NOT_EXISTS_OR_NOT_ACCESSIBLE[4800]",
# "rowId":0,
# "message":"subscription 1840 does not exist - structure SUBSCRIPTION_NOT_EXISTS_OR_NOT_ACCESSIBLE (code:4800)",
# "localizedMessage":"subscription 1840 does not exist"}


class JistError():
    http_status_code: int
    code: int
    row_id: int = Field(alias="rowId")
    message: str
    localized_message: str = Field(alias="localizedMessage")

    def __init__(self, response: Response):
        self.status_code: int = response.status_code
        # TODO: parsing of error json object to fields
        self.message: str = response.text


class JistOperation(Generic[ContentT]):
    def __init__(self):
        self.content: ContentT = None
        self.error: JistError = None

    @property
    def is_success(self):
        return (
            True
            if (self.error is None) and (self.content is not None)
            else False
        )
