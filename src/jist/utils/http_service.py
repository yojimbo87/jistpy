from requests import (
    get as rget,
    post as rpost,
    delete as rdelete,
    Response
)

host = ""
credentials = ("", "")
pat_token = ""
pat_expiration_duration = 1
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
    # "X-Atlassian-Token": "no-check"
}
request_retry_count = 5


def init(hostname: str, username: str, password: str) -> None:
    global host
    global credentials

    host = hostname
    credentials = (username, password)


def get(endpoint: str) -> Response:
    response = rget(
        host + endpoint,
        headers=headers,
        auth=credentials
    )

    return response


def post(
        endpoint: str,
        data: str,
        pat_token: str = None,
        credentials: tuple[str, str] = None) -> Response:
    if pat_token:
        headers["Authorization"] = f"Bearer {pat_token}"

    response = rpost(
        host + endpoint,
        headers=headers,
        auth=credentials if credentials else None,
        data=data
    )

    return response


def delete(endpoint: str) -> Response:
    response = rdelete(
        host + endpoint,
        headers=headers,
        auth=credentials
    )

    return response


def to_json(response: Response) -> any:
    return (
        response.json()
        if len(response.text) > 0
        else None
    )
