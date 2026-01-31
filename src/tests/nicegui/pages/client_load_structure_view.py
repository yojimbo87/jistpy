from nicegui import ui
from jist.utils import Secret
from jist import JIST


def client_load_structure_view_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve structure data with default view attributes
    structure = jist.load_structure_view(613)

    # Setup web interface
    columns = []
    for k, v in structure.attribute_specs.items():
        columns.append(
            {
                'name': k,
                'label': v.id,
                'field': k,
                'align': 'left'
            }
        )
    rows = []
    for structure_row in structure.rows:
        row = {
            "row_id": structure_row.id
        }

        for i_attr, attr_id in enumerate(structure_row.attribute_ids):
            row[attr_id] = structure_row.values[i_attr]

        rows.append(row)

    # Setup table
    ui.table(columns=columns, rows=rows, row_key='row_id')
    # Print count of forest items
    ui.label(f"Items count: {len(structure.rows)}")
