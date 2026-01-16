from pydantic import BaseModel, Field, ConfigDict

class ForestSpec(BaseModel):
    structure_id: int = Field(alias="structureId")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)

class Version(BaseModel):
    signature: int
    version: int

class Forest(BaseModel):
    spec: ForestSpec
    formula: str
    item_types: dict = Field(alias = "itemTypes")
    version: Version
