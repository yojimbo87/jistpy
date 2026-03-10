from nicegui import ui
from jist.utils import Secret
from jist import JIST, AuthenticationMode


def rest_get_pat_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    message = ""

    try:
        jist = JIST(  # noqa: F841
            hostname=secret.hostname,
            username=secret.username,
            password=secret.password,
            authentication_mode=AuthenticationMode.PAT
        )
        message = "PAT authentication was successful"
    except Exception as exception:
        message = repr(exception)

    # Setup web interface
    ui.code(message).style('width: 800px')
