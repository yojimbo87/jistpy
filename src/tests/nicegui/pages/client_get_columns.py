import polars as pl
from nicegui import ui
from jist.utils import Secret
from jist import JIST, ColumnKey


def client_get_columns_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(hostname=secret.hostname, pat=secret.pat)

    # Retrieve structure data
    operation = (
        jist.structure(575)
            .load_view()  # Loads default view if view ID is not given
    )

    if operation.failed:
        ui.code(operation.error.message).style('width: 800px')
        return

    data = operation.content.get_columns(
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
