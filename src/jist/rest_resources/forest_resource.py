from pydantic import TypeAdapter
from jist.specs.forest_spec import ForestSpec, ForestResponse
from jist.utils import http_service as http, forest_parser


def get_forest(structure_id: int) -> ForestResponse:
    forest_spec = ForestSpec(structure_id=structure_id)

    request_json_data = forest_spec.model_dump_json()
    response = http.post("rest/structure/2.0/forest/latest", request_json_data)

    response_json_data = response.json()
    validated_data = TypeAdapter(ForestResponse).validate_python(
        response_json_data
    )

    validated_data.components = forest_parser.parse_formula(
        validated_data.formula
    )

    return validated_data
