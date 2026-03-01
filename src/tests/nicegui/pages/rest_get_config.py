from nicegui import ui
from jist.utils import Secret
from jist import JIST


def rest_get_config_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(hostname=secret.hostname, pat=secret.pat)

    # Retrieve Jira config data
    operation = jist.rest_api.get_config()

    operation_result = (
        operation.content.model_dump_json(indent=2)
        if operation.succeeded
        else operation.error.message
    )

    # Setup web interface
    ui.code(operation_result).style('width: 800px')
