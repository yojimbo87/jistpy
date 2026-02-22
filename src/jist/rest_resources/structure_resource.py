from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs import StructureResponse, StructuresResponse
from jist.utils import http_service as http


def get_structures() -> JistOperation[StructuresResponse]:
    response = http.get("rest/structure/2.0/structure")
    operation = JistOperation[list[StructureResponse]](response.status_code)
    response_json_data = http.parse_json_content(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(
                StructuresResponse
            ).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation


def get_structure(structure_id: int) -> JistOperation[StructureResponse]:
    response = http.get(f"rest/structure/2.0/structure/{structure_id}")
    operation = JistOperation[StructureResponse](response.status_code)
    response_json_data = http.parse_json_content(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(StructureResponse).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
