from jist.specs import (
    AttributeSpec,
    ColumnSpec
)


class StructureColumn:
    def __init__(
            self,
            id: str,
            columns_spec: ColumnSpec,
            attribute_spec: AttributeSpec,
            values: list[any]):
        self.id: str = id
        self.column_spec = columns_spec
        self.attribute_spec = attribute_spec
        self.values = values


class Structure:
    def __init__(self, id: int):
        self.id: int = id
        self.columns: dict[str, StructureColumn] = {}

    def get_columns(
            self,
            *column_names: str) -> dict[str, list[any]]:
        data: dict[str, list[any]] = {}

        # Iterate column names argument
        for column_name in column_names:
            # Iterate structure columns
            for column_id, column in self.columns.items():
                # Find desired column with specified name
                if column.column_spec.name == column_name:
                    # Load data into dictionary under column name field
                    if column_name not in data:
                        data[column_name] = column.values

        return data
