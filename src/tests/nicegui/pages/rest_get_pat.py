from nicegui import ui
from jist.utils import Secret
from jist import JIST


def rest_get_pat_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(
        hostname=secret.hostname,
        username=secret.username,
        password=secret.password
    )

    # Authenticate user
    operation = jist.request_pat(secret.username, secret.password)

    operation_result = (
        operation.content.model_dump_json(indent=2)
        if operation.is_success
        else operation.error.message
    )

    # Setup web interface
    ui.code(operation_result).style('width: 800px')
