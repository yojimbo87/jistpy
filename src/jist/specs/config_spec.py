from pydantic import BaseModel, Field


class JiraField(BaseModel):
    id: str
    name: str
    type: str = Field(default=None)
    custom_id: int = Field(default=None, alias="customId")
    custom: str = Field(default=None)
    visible: bool


class ConfigResponse(BaseModel):
    structure_version: str = Field(alias="structureVersion")
    jira_version: str = Field(alias="jiraVersion")
    jiraFields: list[JiraField]
