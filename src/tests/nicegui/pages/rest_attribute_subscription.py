from functools import partial
from nicegui import ui, run
from jist.utils import Secret
from jist import JIST
from jist.specs import (
    AttributeSpec,
    AttributeId,
    AttributeValueFormat,
    SubscriptionData
)


def rest_attribute_subscription_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)
    values_update = True
    values_timeout = 500
    skip_loading = False

    # Retrieve value data
    create_subscription_data = jist.rest_api.create_subscription(
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
        values_update=values_update,
        values_timeout=values_timeout
    )

    ui.code(
        create_subscription_data.model_dump_json(indent=2)
    ).style('width: 800px')

    ui.button(
        "Poll subscription",
        on_click=partial(
            handle_poll_subscription,
            jist,
            create_subscription_data,
            values_update,
            values_timeout,
            skip_loading
        )
    )


async def handle_poll_subscription(
    jist: JIST,
    subscription_data: SubscriptionData,
    values_update: bool,
    values_timeout: int,
    skip_loading: bool
):
    poll_subscription_data = await run.io_bound(
        jist.rest_api.poll_subscription,
        subscription_data.id,
        subscription_data.values_update.version.signature,
        subscription_data.values_update.version.version,
        values_update,
        values_timeout,
        skip_loading
    )

    ui.code(
        poll_subscription_data.model_dump_json(indent=2)
    ).style('width: 800px')
