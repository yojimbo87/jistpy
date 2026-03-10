from jist.authentication_mode import AuthenticationMode
from requests import (
    get as rget,
    post as rpost,
    delete as rdelete,
    Response
)

jira_authentication_mode: AuthenticationMode = None
jira_hostname: str = None
jira_credentials: tuple[str, str] = None
jira_pat: str = None
jira_pat_expiration_duration = 90
# So far only used during value retrieval to retry long running jobs
request_retry_count = 5
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
    # "X-Atlassian-Token": "no-check"
}


def init(
        hostname: str,
        username: str = None,
        password: str = None,
        pat: str = None,
        pat_expiration_duration: int = 90,
        authentication_mode=AuthenticationMode.PAT) -> None:
    global jira_hostname
    global jira_credentials
    global jira_pat
    global jira_pat_expiration_duration

    jira_hostname = hostname
    jira_authentication_mode = authentication_mode
    jira_pat_expiration_duration = pat_expiration_duration

    # Handle selected authentication mode
    match jira_authentication_mode:
        # https://developer.atlassian.com/server/jira/platform/personal-access-token/
        case AuthenticationMode.PAT:
            # If PAT token is supplied, it can be applied
            # If PAT token is not supplied, JIST class will try to send
            # authentication request
            if pat:
                set_pat(pat)
        # https://developer.atlassian.com/server/jira/platform/basic-authentication/
        case AuthenticationMode.BASIC:
            # If username and password are supplied, credentials can be set
            if username and password:
                jira_credentials = (username, password)


def set_pat(pat: str) -> None:
    jira_pat = pat
    headers["Authorization"] = f"Bearer {jira_pat}"


def get(endpoint: str) -> Response:
    response = rget(
        jira_hostname + endpoint,
        headers=headers,
        auth=jira_credentials
    )

    return response


def post(
        endpoint: str,
        data: str) -> Response:
    response = rpost(
        jira_hostname + endpoint,
        headers=headers,
        auth=jira_credentials,
        data=data
    )

    return response


def delete(endpoint: str) -> Response:
    response = rdelete(
        jira_hostname + endpoint,
        headers=headers,
        auth=jira_credentials
    )

    return response


def to_json(response: Response) -> any:
    return (
        response.json()
        if len(response.text) > 0
        else None
    )
