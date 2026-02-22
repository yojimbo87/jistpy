from requests import (
    get as rget,
    post as rpost,
    delete as rdelete,
    Response
)

host = ""
credentials = ("", "")
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


def post(endpoint: str, data: str) -> Response:
    response = rpost(
        host + endpoint,
        headers=headers,
        auth=credentials,
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


def parse_json_content(response: Response) -> str:
    return (
        response.json()
        if len(response.text) > 0
        else None
    )
