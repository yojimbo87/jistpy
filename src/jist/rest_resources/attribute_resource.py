from pydantic import TypeAdapter
from jist.specs import SubscriptionWindow, SubscriptionData
from jist.utils import http_service as http


def create_subscription(
    subscription_window: SubscriptionWindow,
    values_update: bool = False,
    values_timeout: int = 1000
) -> SubscriptionData:
    request_json_data = subscription_window.model_dump_json(exclude_none=True)
    response = http.post(
        (
            f"rest/structure/2.0/attribute/subscription"
            f"?valuesUpdate={values_update}"
            f"&valuesTimeout={values_timeout}"
        ),
        request_json_data
    )
    json_data = response.json()
    validated_data = TypeAdapter(SubscriptionData).validate_python(
        json_data
    )

    return validated_data


def poll_subscription(
    subscription_id: int,
    signature: int,
    version: int,
    values_update: bool = False,
    values_timeout: int = 1000,
    skip_loading: bool = False
) -> SubscriptionData:
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
    json_data = response.json()
    validated_data = TypeAdapter(SubscriptionData).validate_python(
        json_data
    )

    return validated_data
