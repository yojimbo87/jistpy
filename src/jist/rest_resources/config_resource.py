from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs.config_spec import ConfigResponse
from jist.utils import http_service as http


def get_config() -> JistOperation[ConfigResponse]:
    response = http.get("rest/structure/1.0/config/widget")
    operation = JistOperation[ConfigResponse](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(ConfigResponse).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
