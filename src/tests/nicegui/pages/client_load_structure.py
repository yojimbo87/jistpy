from nicegui import ui
from jist.utils import Secret
from jist import JIST, AttributeId, AttributeValueFormat, AttributeSpec


def client_load_structure_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    attribute_specs = [
        AttributeSpec(
            id=AttributeId.SUMMARY,
            format=AttributeValueFormat.TEXT
        ),
        AttributeSpec(
            id=AttributeId.STATUS,
            format=AttributeValueFormat.TEXT
        ),
        AttributeSpec(
            id=AttributeId.LABELS,
            format=AttributeValueFormat.TEXT
        )
    ]

    # Retrieve structure data with specified attributes
    structure = jist.load_structure(613, attribute_specs)

    # Setup web interface
    columns = []
    columns.append(
        {
            'name': "row_id",
            'label': "Row ID",
            'field': "row_id",
            'align': 'left'
        }
    )
    columns.append(
        {
            'name': "depth",
            'label': "Depth",
            'field': "depth",
            'align': 'left'
        }
    )
    columns.append(
        {
            'name': "item_type",
            'label': "Item type",
            'field': "item_type",
            'align': 'left'
        }
    )
    columns.append(
        {
            'name': "item_id",
            'label': "Item ID",
            'field': "item_id",
            'align': 'left'
        }
    )
    columns.append(
        {
            'name': "issue_id",
            'label': "Issue ID",
            'field': "issue_id",
            'align': 'left'
        }
    )

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
            "row_id": structure_row.id,
            "depth": structure_row.depth,
            "item_type": structure_row.item_type.name,
            "item_id": structure_row.item_id,
            "issue_id": structure_row.issue_id
        }

        for i_column, column in enumerate(structure.columns):
            csid = column.csid
            row[csid] = structure_row.values[i_column]

        rows.append(row)

    # Setup table
    ui.table(columns=columns, rows=rows, row_key='row_id')
    # Print count of forest items
    ui.label(f"Items count: {len(structure.rows)}")
