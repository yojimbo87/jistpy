from pydantic import TypeAdapter
from jist.jist_operation import JistOperation, JistError
from jist.specs import SubscriptionWindow, SubscriptionData
from jist.utils import http_service as http


def create_subscription(
    subscription_window: SubscriptionWindow,
    values_update: bool = False,
    values_timeout: int = 1000
) -> JistOperation[SubscriptionData]:
    request_json_data = subscription_window.model_dump_json(exclude_none=True)
    response = http.post(
        (
            f"rest/structure/2.0/attribute/subscription"
            f"?valuesUpdate={values_update}"
            f"&valuesTimeout={values_timeout}"
        ),
        request_json_data
    )
    operation = JistOperation[SubscriptionData](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(SubscriptionData).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation


def poll_subscription(
    subscription_id: int,
    signature: int,
    version: int,
    values_update: bool = False,
    values_timeout: int = 1000,
    skip_loading: bool = False
) -> JistOperation[SubscriptionData]:
    response = http.get(
        (
            f"rest/structure/2.0/attribute/subscription/{subscription_id}"
            f"?valuesUpdate={values_update}"
            f"&valuesTimeout={values_timeout}"
            f"&signature={signature}"
            f"&version={version}"
            f"&skipLoading={skip_loading}"
        )
    )
    operation = JistOperation[SubscriptionData](response.status_code)
    response_json_data = http.to_json(response)

    match response.status_code:
        case 200:
            operation.content = TypeAdapter(SubscriptionData).validate_python(
                response_json_data
            )
        case _:
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation


def delete_subscription(subscription_id: int) -> JistOperation[bool]:
    response = http.delete(
        f"rest/structure/2.0/attribute/subscription/{subscription_id}"
    )
    operation = JistOperation[bool](response.status_code)

    match response.status_code:
        case 200:
            operation.content = True
        case _:
            response_json_data = http.to_json(response)
            operation.error = TypeAdapter(JistError).validate_python(
                response_json_data
            )

    return operation
