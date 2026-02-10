import polars as pl
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

    data = {}
    columns = []
    for column in structure.columns:
        data[column.id] = column.values

        columns.append({
            "name": column.column_spec.name,
            "label": column.column_spec.name,
            "field": column.id,
            "align": "left"
        })
    df = pl.DataFrame(data=data)

    # Setup web interface
    ui.table.from_polars(df, columns=columns).style('width: 1600px')
