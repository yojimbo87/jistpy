from pydantic import BaseModel, Field, ConfigDict
from jist.specs.forest_spec import ForestSpec


class AttributeSpec(BaseModel):
    id: str
    format: str
    params: dict = Field(default=None)


class ValueRequestItem(BaseModel):
    forest_spec: ForestSpec = Field(alias="forestSpec")
    rows: list[int]
    attributes: list[AttributeSpec]

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class ValueRequest(BaseModel):
    requests: list[ValueRequestItem]


class AttributeData(BaseModel):
    attribute: AttributeSpec
    values: list
    trail_mode: str = Field(default=None, alias="trailMode")
    trails: list[str]

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class Version(BaseModel):
    signature: int
    version: int


class ValueResponseItem(BaseModel):
    forest_spec: ForestSpec = Field(alias="forestSpec")
    rows: list[int]
    data: list[AttributeData]
    forest_version: Version = Field(alias="forestVersion")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class ValueResponse(BaseModel):
    responses: list[ValueResponseItem]
    item_types: dict = Field(alias="itemTypes")
    items_version: Version = Field(alias="itemsVersion")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)
