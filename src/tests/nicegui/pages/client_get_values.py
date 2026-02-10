import polars as pl
from nicegui import ui
from jist.utils import Secret
from jist import JIST


def client_get_values_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve structure data
    structure = jist.load_structure_view(613)
    data = structure.get_values(
        "Summaryaa",
        "Status",
        "Theme labels",
        include_row_ids=True,
        include_row_item_types=True
    )
    df = pl.DataFrame(data=data)

    # Setup web interface
    ui.table.from_polars(df).style('width: 1600px')
