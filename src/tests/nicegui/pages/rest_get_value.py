from nicegui import ui
from jist.utils import Secret
from jist import JIST
from jist.specs import AttributeSpec, AttributeId, AttributeValueFormat


def rest_get_value_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve value data
    operation = jist.rest_api.get_value(
        600,
        [807094, 807096, 807086, 9993, 9999, 10023],
        [
            AttributeSpec(
                id=AttributeId.SUMMARY,
                format=AttributeValueFormat.TEXT
            )
        ]
    )

    operation_result = (
        operation.content.model_dump_json(indent=2)
        if operation.is_success
        else operation.error.message
    )

    # Setup web interface
    ui.code(operation_result).style('width: 800px')
