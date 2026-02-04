from nicegui import ui
from jist.utils import Secret
from jist import JIST


def rest_get_config_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve Jira config data
    data = jist.rest_api.get_config()
    pretty_json = data.model_dump_json(indent=2)

    # Setup web interface
    ui.code(pretty_json).style('width: 800px')
