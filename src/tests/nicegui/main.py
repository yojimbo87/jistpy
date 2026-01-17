import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from pydantic import TypeAdapter
from nicegui import ui
from utils import Secret
from jist import JIST
from specs.forest_spec import ForestComponent

secret = Secret("secret.ini", "Credentials2")
jist = JIST(secret.hostname, secret.username, secret.password)
data = jist.get_forest(600)

columns = [
    {'name': 'raw_component', 'label': 'Raw component', 'field': 'raw_component', 'align': 'left'},
    {'name': 'row_id', 'label': 'Row ID', 'field': 'row_id', 'required': True, 'align': 'right'},
    {'name': 'row_depth', 'label': 'Row depth', 'field': 'row_depth'},
    {'name': 'item_type', 'label': 'Item type', 'field': 'item_type'},
    {'name': 'item_id', 'label': 'Item ID', 'field': 'item_id'},
    {'name': 'issue_id', 'label': 'Issue ID', 'field': 'issue_id'},
    {'name': 'row_semantic', 'label': 'Row semantic', 'field': 'row_semantic'}
]

ta = TypeAdapter(list[ForestComponent])
rows = ta.dump_python(data.components)

ui.table(columns=columns, rows=rows, row_key='row_id')

ui.run()