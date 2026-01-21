from pydantic import TypeAdapter
from specs import ValueRequest, ValueResponse
from utils import http_service as http


def get_value(request: ValueRequest):
    request_json_data = request.model_dump_json(exclude_none=True)
    response = http.post("rest/structure/2.0/value", request_json_data)

    response_json_data = response.json()
    validated_data = TypeAdapter(ValueResponse).validate_python(
        response_json_data
    )

    return validated_data
