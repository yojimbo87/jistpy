from datetime import datetime
from functools import partial
from nicegui import ui, run
from jist.utils import Secret
from jist import JIST
from jist.specs import (
    AttributeSpec,
    AttributeId,
    AttributeValueFormat
)


def rest_attribute_subscription_content() -> None:
    global label_element
    global code_element
    global jist
    global values_update
    global values_timeout
    global skip_loading
    global subscription_data
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)
    values_update = True
    values_timeout = 500
    skip_loading = False

    ui.button(
        "Create subscription",
        on_click=partial(
            handle_create_subscription
        )
    )

    ui.button(
        "Poll subscription",
        on_click=partial(
            handle_poll_subscription
        )
    )

    ui.button(
        "Delete subscription",
        on_click=partial(
            handle_delete_subscription
        )
    )

    label_element = ui.label("Initializing...")
    code_element = ui.code("Initializing...").style('width: 800px')


async def handle_create_subscription():
    global subscription_data

    label_element.text = (
        f"Requesting create subscription on"
        f" {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )

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
        create_operation.content.model_dump_json(indent=2)
        if create_operation.is_success
        else create_operation.error.message
    )

    subscription_data = create_operation.content
    code_element.content = create_result


async def handle_poll_subscription():
    global subscription_data

    label_element.text = (
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

    subscription_data = poll_operation.content
    code_element.content = poll_result


async def handle_delete_subscription():
    label_element.text = (
        f"Requesting delete subscription {subscription_data.id} on"
        f" {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )

    delete_operation = await run.io_bound(
        jist.rest_api.delete_subscription,
        subscription_data.id
    )

    delete_result = (
        delete_operation.content
        if delete_operation.is_success
        else delete_operation.error.message
    )

    code_element.content = f"Result of delete subscription: {delete_result}"
