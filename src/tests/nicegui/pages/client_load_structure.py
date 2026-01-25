from nicegui import ui
from jist.utils import Secret
from jist import JIST, AttributeSpec


def client_load_structure_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    attribute_specs = [
        AttributeSpec(id="summary", format="text"),
        AttributeSpec(id="status", format="text")
    ]

    # Retrieve structures
    structure = jist.load_structure(613, attribute_specs)

    # Setup web interface
    ui.code(structure.model_dump_json(indent=2)).style('width: 800px')
