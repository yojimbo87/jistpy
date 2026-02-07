from enum import Enum
from pydantic import BaseModel, Field
from jist.specs.value_spec import AttributeSpec


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


class StructureColumn(BaseModel):
    csid: str
    key: StructureColumnKey
    name: str = Field(default="")
    attribute_spec: AttributeSpec


class StructureRow(BaseModel):
    id: int
    # TODO: generic type or any?
    values: list[str] = Field(default=[])


class Structure(BaseModel):
    id: int
    columns: list[StructureColumn] = Field(default=[])
    rows: list[StructureRow] = Field(default=[])
