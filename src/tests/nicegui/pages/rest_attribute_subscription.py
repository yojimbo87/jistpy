from datetime import datetime
from functools import partial
import json
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
    create_operation = jist.rest_api.create_subscription(
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

    create_result = (
        #json.dumps(create_operation.content, indent=2)
        create_operation.content.model_dump_json(indent=2)
        if create_operation.is_success
        else create_operation.error.message
    )

    ui.code(create_result).style('width: 800px')

    ui.button(
        "Poll subscription",
        on_click=partial(
            handle_poll_subscription,
            jist,
            create_operation.content,
            values_update,
            values_timeout,
            skip_loading
        )
    )

    ui.button(
        "Delete subscription",
        on_click=partial(
            handle_delete_subscription,
            jist,
            create_operation.content.id,
        )
    )


async def handle_poll_subscription(
    jist: JIST,
    subscription_data: SubscriptionData,
    values_update: bool,
    values_timeout: int,
    skip_loading: bool
):
    ui.label(
        f"Requesting poll subscription {subscription_data.id} on"
        f" {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )

    poll_operation = await run.io_bound(
        jist.rest_api.poll_subscription,
        subscription_data.id,
        subscription_data.values_update.version.signature,
        subscription_data.values_update.version.version,
        values_update,
        values_timeout,
        skip_loading
    )

    poll_result = (
        poll_operation.content.model_dump_json(indent=2)
        if poll_operation.is_success
        else poll_operation.error.message
    )

    ui.code(poll_result).style('width: 800px')


async def handle_delete_subscription(
    jist: JIST,
    subscription_id: int
):
    ui.label(
        f"Requesting delete subscription {subscription_id} on"
        f" {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )

    delete_operation = await run.io_bound(
        jist.rest_api.delete_subscription,
        subscription_id
    )

    delete_result = (
        delete_operation.content
        if delete_operation.is_success
        else delete_operation.error.message
    )

    ui.code(
        f"Result of delete subscription: {delete_result}"
    ).style('width: 800px')
