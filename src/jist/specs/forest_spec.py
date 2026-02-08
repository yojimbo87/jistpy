from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


# https://apidocs.tempo.io/dc-structure/javadoc/structure/latest/com/almworks/jira/structure/api/item/CoreItemTypes.html
# https://apidocs.tempo.io/dc-structure/javadoc/structure/latest/constant-values.html
class ForestItemType(str, Enum):
    FOLDER = "com.almworks.jira.structure:type-folder"
    GENERATOR = "com.almworks.jira.structure:type-generator"
    ISSUE = "com.almworks.jira.structure:type-issue"


class ForestSpec(BaseModel):
    structure_id: int = Field(alias="structureId")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class Version(BaseModel):
    signature: int
    version: int


class ForestComponent(BaseModel):
    raw_component: str
    row_id: int
    row_depth: int
    item_identity: str
    row_semantic: int
    item_type: int
    item_id: str
    issue_id: int


class ForestResponse(BaseModel):
    spec: ForestSpec
    formula: str
    components: list[ForestComponent] = Field(default=None)
    item_types: dict = Field(alias="itemTypes")
    version: Version
