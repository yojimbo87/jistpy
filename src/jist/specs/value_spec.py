from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from jist.specs.forest_spec import ForestSpec


class JiraFieldType(str, Enum):
    any = "any"
    array = "array"
    custom = "custom"
    date = "date"
    datetime = "datetime"
    number = "number"
    option = "option"
    priority = "priority"
    progress = "progress"
    project = "project"
    resolution = "resolution"
    security_level = "securitylevel"
    status = "status"
    string = "string"
    user = "user"
    votes = "votes"
    watches = "watches"


class AttributeValueFormat(str, Enum):
    any = "any"
    boolean = "boolean"
    duration = "duration"
    html = "html"
    id = "id"
    json_array = "json_array"
    json_object = "json_object"
    number = "number"
    order = "order"
    text = "text"
    time = "time"


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
    trails: list[str] = Field(default=[])

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class Version(BaseModel):
    signature: int
    version: int


class ValueResponseItem(BaseModel):
    forest_spec: ForestSpec = Field(alias="forestSpec")
    rows: list[int]
    data: list[AttributeData]
    forest_version: Version = Field(default=None, alias="forestVersion")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class ValueResponse(BaseModel):
    responses: list[ValueResponseItem]
    item_types: dict = Field(default={}, alias="itemTypes")
    items_version: Version = Field(default=None, alias="itemsVersion")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)
