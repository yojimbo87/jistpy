from typing import Generic, TypeVar
from requests import Response
from pydantic import TypeAdapter

ContentT = TypeVar("ContentT")


class JistError():
    status_code: int
    message: str

    def __init__(self, response: Response):
        self.status_code: int = response.status_code
        self.message: str = response.text


class JistOperation(Generic[ContentT]):
    def __init__(self, response: Response):
        self.content: ContentT = None
        self.error: JistError = None

        match response.status_code:
            case 200:
                if len(response.content) > 0:
                    json_data = response.json()
                    
                    # TODO: content is serialized as dict and not as pydantic model
                    self.content = TypeAdapter(ContentT).validate_python(
                        json_data
                    )
                else:
                    self.content = True
            case _:
                self.error = JistError(response)

    @property
    def is_success(self):
        return (
            True
            if (self.error is None) and (self.content is not None)
            else False
        )
