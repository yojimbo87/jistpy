from pydantic import TypeAdapter
from structure_spec import Structure
import http_service as http

def get_structures() -> list[Structure]:
    response = http.get("rest/structure/2.0/structure")
    raw_structures = response.json()["structures"]
    validated_structures = TypeAdapter(list[Structure]).validate_python(raw_structures)

    return validated_structures