from requests import get as rget, post as rpost, Response

host = ""
credentials = ("", "")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
    #"X-Atlassian-Token": "no-check"
}

def init(hostname: str, username: str, password: str) -> None:
    global host
    global credentials

    host = hostname
    credentials = (username, password)

def get(endpoint: str) -> Response:
    response = rget(
        host + endpoint,
        headers = headers,
        auth = credentials
    )

    return response

def post(endpoint: str, data: str) -> Response:
    response = rpost(
        host + endpoint,
        headers = headers,
        auth = credentials,
        data = data
    )

    return response