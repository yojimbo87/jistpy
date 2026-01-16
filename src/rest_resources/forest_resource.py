from pydantic import TypeAdapter
from specs.forest_spec import ForestSpec, ForestComponent, Forest
from utils import http_service as http

def get_forest(structure_id: int) -> Forest:
    forest_spec = ForestSpec(structure_id=structure_id)

    request_json_data = forest_spec.model_dump_json()
    response = http.post("rest/structure/2.0/forest/latest", request_json_data)
    
    response_json_data = response.json()
    validated_data = TypeAdapter(Forest).validate_python(response_json_data)

    validated_data.components = parse_forest_formula(validated_data.formula)

    return validated_data

def parse_forest_formula(formula: str) -> list[ForestComponent]:
    forest_components: list[ForestComponent] = []

    for raw_component in formula.split(","):
        component_parts = raw_component.split(":")

        item_identity = component_parts[2]
        item_type: int = 0
        item_id: str = ""
        issue_id: int = 0
        item_split: list[str] = []

        if "//" in item_identity:
            item_split = item_identity.split("//")
        elif "/" in item_identity:
            item_split = item_identity.split("/")

        if len(item_split) == 2:
            item_type = item_split[0]
            item_id = item_split[1]
        else:
            issue_id = int(item_identity)


        if len(item_split) == 0:
            issue_id = int(item_identity)
        elif len(item_split) == 2:
            item_type = item_split[0]
            item_id = item_split[1]

        forest_components.append(
            ForestComponent(
                raw_component=raw_component,
                row_id=int(component_parts[0]),
                row_depth=int(component_parts[1]),
                row_semantic=int(component_parts[3]) if (len(component_parts) > 3) else 0,
                item_identity=item_identity,
                item_type=item_type,
                item_id=item_id,
                issue_id=issue_id
            )
        )

    return forest_components