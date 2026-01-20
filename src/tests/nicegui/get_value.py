import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from pydantic import TypeAdapter
from nicegui import ui
from utils import Secret
from jist import JIST
from specs import AttributeDefinition
from devtools import pprint

# Setup client
secret = Secret("secret.ini", "Credentials2")
jist = JIST(secret.hostname, secret.username, secret.password)

# Retrieve value data
data = jist.get_value(
    600,
    [807094, 807096, 807086, 9993, 9999, 10023],
    [
        AttributeDefinition(
            id="summary",
            format="text"
        )
    ]
)

ui.json_editor({'content': {'json': data.model_dump()}})

ui.code(data.model_dump_json(indent=2))

ui.run()