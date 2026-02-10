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
    structure = jist.load_structure(613, attribute_specs)

    data = {}
    for column in structure.columns:
        data[column.id] = column.values
    df = pl.DataFrame(data=data)

    # Setup web interface
    ui.table.from_polars(df).style('width: 1600px')
