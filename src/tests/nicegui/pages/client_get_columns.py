import polars as pl
from nicegui import ui
from jist.utils import Secret
from jist import JIST, ColumnKey


def client_get_columns_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve structure data
    structure = jist.load_structure_view(575)
    data = structure.get_columns(
        ColumnKey.ROW_DEPTH,
        "__row_item_type",
        ColumnKey.KEY,
        ColumnKey.SUMMARY,
        "Issue Type",
        "Project",
        "Distribution type"
    )
    df = pl.DataFrame(data=data)

    # Setup web interface
    ui.table.from_polars(df).style('width: 1600px')
