from pydantic import BaseModel, Field


class ColumnSpec(BaseModel):
    # Mandatory property that defines the class of the column, its behavior.
    # As of Structure 2.0, there's a predefined set of supported column keys.
    # In the future, we plan to make it expandable.
    key: str

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
