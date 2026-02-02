from pydantic import TypeAdapter
from jist.specs.config_spec import ConfigResponse
from jist.utils import http_service as http


def get_config() -> ConfigResponse:
    response = http.get("rest/structure/1.0/config/widget")

    response_json_data = response.json()
    validated_data = TypeAdapter(ConfigResponse).validate_python(
        response_json_data
    )

    return validated_data
