import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from nicegui import ui
from utils import Secret
from jist import JIST

# Setup client
secret = Secret("secret.ini", "Credentials2")
jist = JIST(secret.hostname, secret.username, secret.password)

# Retrieve structure data
data = jist.get_structure(600)
pretty_json = data.model_dump_json(indent=2)

# Setup web interface
ui.code(pretty_json)
ui.run()