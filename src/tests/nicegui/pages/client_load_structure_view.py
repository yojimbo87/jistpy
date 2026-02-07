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
    structure = jist.load_structure_view(575)

    # Setup web interface
    columns = []
    for column in structure.columns:
        columns.append(
            {
                'name': column.csid,
                'label': f"{column.name} ({column.csid}, {column.key})",
                'field': column.csid,
                'align': 'left'
            }
        )

    rows = []
    for structure_row in structure.rows:
        row = {
            "row_id": structure_row.id
        }

        for i_column, column in enumerate(structure.columns):
            csid = column.csid
            row[csid] = structure_row.values[i_column]

        rows.append(row)

    # Setup table
    ui.table(
        columns=columns,
        rows=rows,
        row_key='row_id'
    ).style('width: 1600px')
    # Print count of forest items
    ui.label(f"Items count: {len(structure.rows)}")
