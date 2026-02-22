from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs import ValueRequest, ValueResponse
from jist.utils import http_service as http


def get_value(request: ValueRequest) -> JistOperation[ValueResponse]:
    request_json_data = request.model_dump_json(exclude_none=True)

    # Retry the request specified amount of times due to nature of value REST
    # API call, which will return objecti with jobId field if the operation
    # wasn't finished yet
    for i in range(http.request_retry_count):
        response = http.post("rest/structure/2.0/value", request_json_data)
        operation = JistOperation[ValueResponse](response.status_code)
        response_json_data = http.to_json(response)

        match response.status_code:
            case 200:
                # Proceed with processing of response data only once it
                # doesn't contain jobId field, indicating that the response
                # contain relevant data structure
                if "jobId" not in response_json_data:
                    operation.content = TypeAdapter(
                        ValueResponse
                    ).validate_python(
                        response_json_data
                    )
                    break
            case _:
                operation.error = TypeAdapter(JistError).validate_python(
                    response_json_data
                )
                break

    return operation
