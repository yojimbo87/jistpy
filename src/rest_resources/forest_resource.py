from pydantic import TypeAdapter
from specs.forest_spec import ForestSpec, Forest
import http_service as http

def get_forest(structure_id: int) -> Forest:
    forest_spec = ForestSpec(structure_id=structure_id)

    request_json_data = forest_spec.model_dump_json()
    response = http.post("rest/structure/2.0/forest/latest", request_json_data)
    
    response_json_data = response.json()
    validated_data = TypeAdapter(Forest).validate_python(response_json_data)

    return validated_data