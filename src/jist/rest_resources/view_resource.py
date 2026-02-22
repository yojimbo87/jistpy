from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs import ViewResponse
from jist.utils import http_service as http


def get_default_view(structure_id: int) -> JistOperation[ViewResponse]:
    response = http.get(
        (
            f"rest/structure/1.0/view/default"
            f"?forPage=structure&forStructure={structure_id}"
        )
    )
    operation = JistOperation[ViewResponse](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(
                ViewResponse
            ).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation


def get_view(view_id: int) -> JistOperation[ViewResponse]:
    response = http.get(f"rest/structure/1.0/view/{view_id}")
    operation = JistOperation[ViewResponse](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(
                ViewResponse
            ).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
