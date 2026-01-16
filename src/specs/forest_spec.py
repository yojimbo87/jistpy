from pydantic import BaseModel, Field, ConfigDict

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

class Forest(BaseModel):
    spec: ForestSpec
    formula: str
    components: list[ForestComponent] = Field(default=None)
    item_types: dict = Field(alias = "itemTypes")
    version: Version
