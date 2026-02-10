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
            *column_names: str,
            include_row_ids=False,
            include_row_depths=False,
            include_row_item_types=False,
            include_row_item_ids=False,
            include_row_issue_ids=False) -> dict[str, list[any]]:
        data: dict[str, list[any]]

        if (include_row_ids
                or include_row_depths
                or include_row_item_types
                or include_row_item_ids
                or include_row_issue_ids):
            data = self.get_row_definitions(
                include_row_ids,
                include_row_depths,
                include_row_item_types,
                include_row_item_ids,
                include_row_issue_ids
            )
        else:
            data = {}

        # Iterate column names argument
        for column_name in column_names:
            # Iterate structure columns to find desired column names
            for i_column, column in enumerate(self.columns):
                # Find desired column
                if column.name == column_name:
                    # Load data into dictionary with column name field
                    if column_name not in data:
                        data[column_name] = []

                    for row in self.rows:
                        data[column_name].append(row.values[i_column])

        return data

    '''
    def get_row_definitions(
            self,
            include_row_ids=True,
            include_row_depths=True,
            include_row_item_types=True,
            include_row_item_ids=True,
            include_row_issue_ids=True) -> list[RowDefinition]:
        row_definitions: list[RowDefinition] = {}

        if include_row_ids:
            row_definitions[ColumnKey.ROW_ID] = []
        if include_row_depths:
            row_definitions[ColumnKey.ROW_DEPTH] = []
        if include_row_item_types:
            row_definitions[ColumnKey.ROW_ITEM_TYPE] = []
        if include_row_item_ids:
            row_definitions[ColumnKey.ROW_ITEM_ID] = []
        if include_row_issue_ids:
            row_definitions[ColumnKey.ROW_ISSUE_ID] = []

        for row in self.rows:
            if include_row_ids:
                row_definitions[ColumnKey.ROW_ID].append(row.id)
            if include_row_depths:
                row_definitions[ColumnKey.ROW_DEPTH].append(row.depth)
            if include_row_item_types:
                row_definitions[ColumnKey.ROW_ITEM_TYPE].append(
                    row.item_type.name
                )
            if include_row_item_ids:
                row_definitions[ColumnKey.ROW_ITEM_ID].append(row.item_id)
            if include_row_issue_ids:
                row_definitions[ColumnKey.ROW_ISSUE_ID].append(
                    row.issue_id
                )

        return row_definitions
    '''
