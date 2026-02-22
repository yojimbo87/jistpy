from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs.forest_spec import ForestSpec, ForestResponse
from jist.utils import http_service as http, forest_parser


def get_forest(structure_id: int) -> JistOperation[ForestResponse]:
    forest_spec = ForestSpec(structure_id=structure_id)
    request_json_data = forest_spec.model_dump_json()
    response = http.post("rest/structure/2.0/forest/latest", request_json_data)
    operation = JistOperation[ForestResponse](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(ForestResponse).validate_python(
                response_json_data
            )
            # Formula string needs to be parsed into components
            operation.content.components = forest_parser.parse_formula(
                operation.content.formula
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
