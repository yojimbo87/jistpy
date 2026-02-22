from nicegui import ui
from jist.utils import Secret
from jist import JIST


def rest_get_config_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve Jira config data
    operation = jist.rest_api.get_config()
    
    operation_result = (
        operation.content.model_dump_json(indent=2)
        if operation.is_success
        else operation.error.message
    )

    # Setup web interface
    ui.code(operation_result).style('width: 800px')
