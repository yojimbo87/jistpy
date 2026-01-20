import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from pydantic import TypeAdapter
from nicegui import ui
from utils import Secret
from jist import JIST
from specs import ForestComponent

# Setup client
secret = Secret("secret.ini", "Credentials2")
jist = JIST(secret.hostname, secret.username, secret.password)

# Retrieve forest data
data = jist.get_forest(600)
'''
# Setup table columns based on forest specification
columns = [
    {'name': 'raw_component', 'label': 'Raw component', 'field': 'raw_component', 'align': 'left'},
    {'name': 'row_id', 'label': 'Row ID', 'field': 'row_id', 'required': True, 'align': 'right'},
    {'name': 'row_depth', 'label': 'Row depth', 'field': 'row_depth'},
    {'name': 'item_type', 'label': 'Item type', 'field': 'item_type'},
    {'name': 'item_id', 'label': 'Item ID', 'field': 'item_id', 'align': 'left'},
    {'name': 'issue_id', 'label': 'Issue ID', 'field': 'issue_id'},
    {'name': 'row_semantic', 'label': 'Row semantic', 'field': 'row_semantic'}
]

# Parse forest data into dictionary for loading into the table as rows
ta = TypeAdapter(list[ForestComponent])
rows: list[dict] = ta.dump_python(data.components)

# Setup table
ui.table(columns=columns, rows=rows, row_key='row_id')
# Print count of forest items
ui.label(f"Items count: {len(rows)}")
'''

# Retrieve forest data
data = jist.get_forest(600)
pretty_json = data.model_dump_json(indent=2)

# Setup web interface
ui.code(pretty_json)
ui.run()