from pydantic import TypeAdapter
from specs.structure_spec import Structure
import http_service as http

def get_structures() -> list[Structure]:
    response = http.get("rest/structure/2.0/structure")
    json_data = response.json()["structures"]
    validated_data = TypeAdapter(list[Structure]).validate_python(json_data)

    return validated_data

def get_structure(structure_id: int) -> Structure:
    response = http.get(f"rest/structure/2.0/structure/{structure_id}")
    json_data = response.json()
    validated_data = TypeAdapter(Structure).validate_python(json_data)

    return validated_data