from nicegui import ui
from jist.utils import Secret
from jist import JIST


def client_load_structure_view_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve config (widget)
    jist.load_config()

    # Retrieve structure data with default view attributes
    structure = jist.load_structure_view(613)

    # Setup web interface
    columns = []
    for csid, column in structure.columns.items():
        columns.append(
            {
                'name': csid,
                'label': column.name,
                'field': csid,
                'align': 'left'
            }
        )
    rows = []
    for structure_row in structure.rows:
        row = {
            "row_id": structure_row.id
        }

        # for i_attr, attr_id in enumerate(structure_row.attribute_ids):
        #     row[attr_id] = structure_row.values[i_attr]
        for i_value, value in enumerate(structure_row.values):
            csid = structure_row.csids[i_value]
            row[csid] = value

        rows.append(row)

    # Setup table
    ui.table(
        columns=columns,
        rows=rows,
        row_key='row_id'
    ).style('width: 1600px')
    # Print count of forest items
    ui.label(f"Items count: {len(structure.rows)}")
