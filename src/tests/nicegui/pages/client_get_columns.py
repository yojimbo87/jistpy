import polars as pl
from nicegui import ui
from jist.utils import Secret
from jist import JIST, ColumnKey


def client_get_columns_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve structure data
    structure = jist.load_structure_view(613)
    data = structure.get_columns(
        ColumnKey.ROW_ID.name,
        "ROW_ITEM_TYPE",
        "Summaryaa",
        "Status",
        "Theme labels"
    )
    df = pl.DataFrame(data=data)

    # Setup web interface
    ui.table.from_polars(df).style('width: 1600px')
