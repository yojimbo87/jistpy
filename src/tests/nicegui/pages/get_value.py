from nicegui import ui
from jist.utils import Secret
from jist import JIST
from jist.specs import AttributeDefinition


def get_value_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve value data
    data = jist.rest_api.get_value(
        600,
        [807094, 807096, 807086, 9993, 9999, 10023],
        [
            AttributeDefinition(
                id="summary",
                format="text"
            )
        ]
    )

    ui.code(data.model_dump_json(indent=2)).style('width: 800px')
