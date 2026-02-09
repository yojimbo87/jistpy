import json
from nicegui import ui
from jist.utils import Secret
from jist import JIST


def client_get_values_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve structure data
    structure = jist.load_structure_view(613)
    data = structure.get_values("Summaryaa", "Status")
    s = json.dumps(data, indent=2)

    # Setup web interface
    ui.code(s).style('width: 800px')
