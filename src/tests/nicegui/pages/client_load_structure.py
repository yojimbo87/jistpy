from nicegui import ui
from jist.utils import Secret
from jist import JIST, AttributeSpec


def client_load_structure_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    attribute_specs = [
        AttributeSpec(id="summary", format="text"),
        AttributeSpec(id="status", format="text"),
        AttributeSpec(id="labels", format="text")
    ]

    # Retrieve structure data with specified attributes
    structure = jist.load_structure(613, attribute_specs)

    # Setup web interface
    columns = []
    for attr_spec in structure.attribute_specs:
        columns.append(
            {
                'name': attr_spec.id,
                'label': attr_spec.id,
                'field': attr_spec.id,
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
