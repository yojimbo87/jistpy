import uuid
from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs.pat_spec import PatRequest, PatResponse
from jist.utils import http_service as http


def get_pat() -> JistOperation[PatResponse]:
    # Create token name from jistpy prefix and uuid hex string
    token_name = f"jistpy-{uuid.uuid4().hex}"
    # Create request json object
    request_json_data = PatRequest(
        name=token_name,
        expiration_duration=http.jira_pat_expiration_duration
    ).model_dump_json()

    # TODO: request needs to use credentials in order to retrieve valid PAT

    # Send request
    response = http.post(
        "/rest/pat/latest/tokens",
        request_json_data
    )
    operation = JistOperation[PatResponse](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 201:
            operation.content = TypeAdapter(PatResponse).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
