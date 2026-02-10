from enum import Enum
from pydantic import BaseModel, Field


class ColumnKey(str, Enum):
    ROW_ID = "__row_id"  # Library internal
    ROW_DEPTH = "__row_depth"  # Library internal
    ROW_ITEM_TYPE = "__row_item_type"  # Library internal
    ROW_ITEM_ID = "__row_item_id"  # Library internal
    ROW_ISSUE_ID = "__row_issue_id"  # Library internal
    ACTIONS = "actions"
    FIELD = "field"
    FORMULA = "formula"
    HANDLE = "handle"
    MAIN = "main"
    UNKNOWN = "unknown"  # Placeholder value for undetermined column key


class ColumnSpec(BaseModel):
    # Mandatory property that defines the class of the column, its behavior.
    # As of Structure 2.0, there's a predefined set of supported column keys.
    # In the future, we plan to make it expandable.
    key: ColumnKey

    # Optional property that defines the header of the column in the grid. If
    # not set, default header is used as decided by the column class.
    name: str = Field(default=None)

    # Mandatory property that should be an unique column ID within the view
    # specification. Typically, special columns have special csid while all
    # other columns have numeric incrementing csid.
    csid: str

    # An unbounded map of any parameters that make sense to the specific class
    # of the column.
    params: dict


class ViewSpec(BaseModel):
    columns: list[ColumnSpec]
    column_display_mode: int = Field(alias="columnDisplayMode")
    row_diplay_mode: int = Field(alias="rowDisplayMode")
    pins: list[str]


class ViewResponse(BaseModel):
    id: int
    name: str
    description: str
    spec: ViewSpec
    writable: bool
    adminable: bool
    shared: bool
    shared_with_all: bool = Field(alias="sharedWithAll")
