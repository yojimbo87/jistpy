from pydantic import TypeAdapter
from jist.specs import ValueRequest, ValueResponse
from jist.utils import http_service as http


def get_value(request: ValueRequest) -> ValueResponse:
    request_json_data = request.model_dump_json(exclude_none=True)

    for i in range(http.request_retry_count):
        response = http.post("rest/structure/2.0/value", request_json_data)
        response_json_data = response.json()

        if response.status_code == 200:

            if "jobId" not in response_json_data:
                validated_data = TypeAdapter(ValueResponse).validate_python(
                    response_json_data
                )
                break

    return validated_data
