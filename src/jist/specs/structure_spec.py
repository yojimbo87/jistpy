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


class StructureColumn(BaseModel):
    id: str
    attribute_spec: AttributeSpec = Field(default=None)
    # TODO: generic type or any?
    data: str = Field(default=None)


class StructureRow(BaseModel):
    id: int
    columns: dict = Field(default={})


class Structure(BaseModel):
    id: int
    rows: dict = Field(default={})
