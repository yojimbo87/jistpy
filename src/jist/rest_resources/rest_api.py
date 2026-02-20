from ..jist_operation import JistOperation
from jist.rest_resources import (
    config_resource,
    structure_resource,
    forest_resource,
    value_resource,
    view_resource,
    attribute_resource
)
from jist.specs import (
    ConfigResponse,
    StructureResponse,
    ForestSpec,
    ForestResponse,
    AttributeSpec,
    ValueRequestItem,
    ValueRequest,
    ValueResponse,
    ViewResponse,
    SubscriptionWindow,
    SubscriptionData
)


def get_config() -> ConfigResponse:
    response = config_resource.get_config()

    return response


def get_structures() -> list[StructureResponse]:
    response = structure_resource.get_structures()

    return response


def get_structure(structure_id: int) -> StructureResponse:
    response = structure_resource.get_structure(structure_id)

    return response


def get_forest(structure_id: int) -> ForestResponse:
    response = forest_resource.get_forest(structure_id)

    return response


def get_value(
    structure_id: int,
    rows: list[int],
    attributes: list[AttributeSpec]
) -> ValueResponse:
    request = ValueRequest(
        requests=[
            ValueRequestItem(
                forestSpec=ForestSpec(structure_id=structure_id),
                rows=rows,
                attributes=attributes
            )
        ]
    )

    response = value_resource.get_value(request)

    return response


def get_default_view(structure_id: int) -> ViewResponse:
    response = view_resource.get_default_view(structure_id)

    return response


def get_view(view_id: int) -> ViewResponse:
    response = view_resource.get_view(view_id)

    return response


def create_subscription(
    structure_id: int,
    rows: list[int],
    attributes: list[AttributeSpec],
    values_update: bool = False,
    values_timeout: int = 1000
) -> JistOperation[SubscriptionData]:
    subscription_window = SubscriptionWindow(
        forestSpec=ForestSpec(structureId=structure_id),
        rows=rows,
        attributes=attributes
    )

    return attribute_resource.create_subscription(
        values_update=values_update,
        values_timeout=values_timeout,
        subscription_window=subscription_window
    )


def poll_subscription(
    subscription_id: int,
    signature: int,
    version: int,
    values_update: bool = False,
    values_timeout: int = 1000,
    skip_loading: bool = False
) -> JistOperation[SubscriptionData]:
    return attribute_resource.poll_subscription(
        subscription_id=subscription_id,
        signature=signature,
        version=version,
        values_update=values_update,
        values_timeout=values_timeout,
        skip_loading=skip_loading
    )


def delete_subscription(subscription_id: int) -> JistOperation[bool]:
    return attribute_resource.delete_subscription(subscription_id)
