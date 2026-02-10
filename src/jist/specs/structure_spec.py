from enum import Enum
from pydantic import BaseModel, Field
from jist.specs.forest_spec import ItemType
from jist.specs.value_spec import AttributeSpec


class RowConstants(str, Enum):
    ROW_IDS = "__row_ids"
    ROW_DEPTHS = "__row_depths"
    ROW_ITEM_TYPES = "__row_item_types"
    ROW_ITEM_IDS = "__row_item_ids"
    ROW_ISSUE_IDS = "__row_issue_ids"


class Permission(BaseModel):
    rule: str
    subject: str = Field(default=None)
    level: str = Field(default=None)
    username: str = Field(default=None)
    structure_id: int = Field(default=None, alias="structureId")
    project_id: int = Field(default=None, alias="projectId")
    group_id: int = Field(default=None, alias="groupId")
    role_id: int = Field(default=None, alias="roleId")
    code: int = Field(default=None)
    error: str = Field(default=None)
    issue_id: int = Field(default=None, alias="issueId")
    message: str = Field(default=None)
    localized_message: str = Field(default=None, alias="localizedMessage")


class StructureResponse(BaseModel):
    id: int
    name: str
    description: str = Field(default=None)
    read_only: bool = Field(default=None, alias="readOnly")
    edit_requires_parent_issue_permission: bool = Field(
        default=None,
        alias="editRequiresParentIssuePermission"
    )
    owner: str = Field(default=None)
    permissions: list[Permission] = Field(default=None)


class StructureColumnKey(str, Enum):
    ACTIONS = "actions"
    FIELD = "field"
    FORMULA = "formula"
    HANDLE = "handle"
    MAIN = "main"
    UNKNOWN = "unknown"  # Placeholder value for undetermined column key


class StructureColumn(BaseModel):
    csid: str
    key: StructureColumnKey
    name: str = Field(default="")
    attribute_spec: AttributeSpec


class StructureRow(BaseModel):
    id: int
    depth: int
    item_type: ItemType
    item_id: str
    issue_id: int
    # TODO: generic type or any?
    values: list[str] = Field(default=[])


class Structure(BaseModel):
    id: int
    columns: list[StructureColumn] = Field(default=[])
    rows: list[StructureRow] = Field(default=[])

    def get_row_definitions(
            self,
            include_row_ids=True,
            include_row_depths=True,
            include_row_item_types=True,
            include_row_item_ids=True,
            include_row_issue_ids=True) -> dict[str, list[any]]:
        row_definitions: dict[str, list] = {}

        if include_row_ids:
            row_definitions[RowConstants.ROW_IDS] = []
        if include_row_depths:
            row_definitions[RowConstants.ROW_DEPTHS] = []
        if include_row_item_types:
            row_definitions[RowConstants.ROW_ITEM_TYPES] = []
        if include_row_item_ids:
            row_definitions[RowConstants.ROW_ITEM_IDS] = []
        if include_row_issue_ids:
            row_definitions[RowConstants.ROW_ISSUE_IDS] = []

        for row in self.rows:
            if include_row_ids:
                row_definitions[RowConstants.ROW_IDS].append(row.id)
            if include_row_depths:
                row_definitions[RowConstants.ROW_DEPTHS].append(row.depth)
            if include_row_item_types:
                row_definitions[RowConstants.ROW_ITEM_TYPES].append(
                    row.item_type.name
                )
            if include_row_item_ids:
                row_definitions[RowConstants.ROW_ITEM_IDS].append(row.item_id)
            if include_row_issue_ids:
                row_definitions[RowConstants.ROW_ISSUE_IDS].append(
                    row.issue_id
                )

        return row_definitions

    def get_values(
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
