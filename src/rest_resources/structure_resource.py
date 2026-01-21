from pydantic import TypeAdapter
from specs import StructureResponse
from utils import http_service as http


def get_structures() -> list[StructureResponse]:
    response = http.get("rest/structure/2.0/structure")
    json_data = response.json()["structures"]
    validated_data = TypeAdapter(list[StructureResponse]).validate_python(
        json_data
    )

    return validated_data


def get_structure(structure_id: int) -> StructureResponse:
    response = http.get(f"rest/structure/2.0/structure/{structure_id}")
    json_data = response.json()
    validated_data = TypeAdapter(StructureResponse).validate_python(json_data)

    return validated_data
