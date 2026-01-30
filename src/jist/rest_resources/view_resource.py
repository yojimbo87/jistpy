from pydantic import TypeAdapter
from jist.specs import ViewResponse
from jist.utils import http_service as http


def get_default_view(structure_id: int) -> ViewResponse:
    url_base = "rest/structure/1.0/view/default"
    url_query_string = f"?forPage=structure&forStructure={structure_id}"

    response = http.get(f"{url_base}{url_query_string}")
    json_data = response.json()
    validated_data = TypeAdapter(ViewResponse).validate_python(json_data)

    return validated_data
