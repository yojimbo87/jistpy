from nicegui import ui
from jist.utils import Secret
from jist import JIST
from jist.specs import AttributeSpec, AttributeId, AttributeValueFormat


def rest_attribute_subscription_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve value data
    data = jist.rest_api.create_subscription(
        structure_id=613,
        rows=[809240, 83425],
        attributes=[
            AttributeSpec(
                id=AttributeId.SUMMARY,
                format=AttributeValueFormat.TEXT
            ),
            AttributeSpec(
                id=AttributeId.STATUS,
                format=AttributeValueFormat.TEXT
            )
        ],
        values_update=True,
        values_timeout=500
    )

    ui.code(data.model_dump_json(indent=2)).style('width: 800px')
