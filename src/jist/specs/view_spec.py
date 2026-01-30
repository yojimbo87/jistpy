from pydantic import BaseModel, Field


class ColumnSpec(BaseModel):
    key: str
    name: str = Field(default=None)
    csid: str
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
