from pydantic import TypeAdapter
from nicegui import ui
from jist.utils import Secret
from jist import JIST, StructureResponse


def rest_get_structures_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve structures
    data = jist.rest_api.get_structures()

    # Parse list of structures into pretty json string
    ta = TypeAdapter(list[StructureResponse])
    pretty_json = ta.dump_json(data, indent=2).decode()

    # Setup web interface
    ui.code(pretty_json).style('width: 800px')
