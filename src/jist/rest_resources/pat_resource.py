import uuid
from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs.pat_spec import PatRequest, PatResponse
from jist.utils import http_service as http


def get_token(
        username: str,
        password: str,
        token_expiration_duration: int) -> JistOperation[PatResponse]:
    token_name = f"jistpy-{uuid.uuid4().hex}"
    request_json_data = PatRequest(
        name=token_name,
        expiration_duration=token_expiration_duration
    ).model_dump_json()
    response = http.post(
        "/rest/pat/latest/tokens",
        request_json_data,
        credentials=(username, password)
    )
    operation = JistOperation[PatResponse](response.status_code)

    match response.status_code:
        case 201:
            operation.content = PatResponse(
                token_name=token_name,
                token=response.text
            )
        case _:
            response_json_data = http.to_json(response)
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
