import polars as pl
from nicegui import ui
from jist.utils import Secret
from jist import JIST


def client_load_structure_view_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(hostname=secret.hostname, pat=secret.pat)

    # Retrieve structure data with default view attributes
    operation = (
        jist.structure(575)
            .with_rows([795740, 77683, 77735])
            .with_row_metadata(False)
            .load_view()  # Loads default view if view ID is not given
    )

    if operation.failed:
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
