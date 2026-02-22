import polars as pl
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
    operation = jist.load_structure(613, attribute_specs)

    if operation.is_success is False:
        ui.code(operation.error.message).style('width: 800px')
        return

    data = {}
    columns = []
    for column_id, column in operation.content.columns.items():
        data[column_id] = column.values

        label = (
            f"{column.column_spec.name} "
            f"({column.id}, {column.column_spec.key.name})"
        )
        if column.attribute_spec:
            label += (
                f", ({column.attribute_spec.id.name}, "
                f"{column.attribute_spec.format.name})"
            )

        columns.append({
            "name": column.column_spec.name,
            "label": label,
            "field": column.id,
            "align": "left"
        })
    df = pl.DataFrame(data=data)

    # Setup web interface
    ui.table.from_polars(df, columns=columns).style('width: 1600px')
