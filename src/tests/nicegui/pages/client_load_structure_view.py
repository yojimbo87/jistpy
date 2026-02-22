import polars as pl
from nicegui import ui
from jist.utils import Secret
from jist import JIST


def client_load_structure_view_content() -> None:
    # Setup client
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(secret.hostname, secret.username, secret.password)

    # Retrieve config (widget)
    config_operation = jist.load_config()

    if config_operation.is_success is False:
        ui.code(config_operation.error.message).style('width: 800px')
        return

    # Retrieve structure data with default view attributes
    operation = jist.load_structure_view(575)

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
