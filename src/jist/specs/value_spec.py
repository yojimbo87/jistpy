from enum import Enum
import json
from pydantic import BaseModel, Field, ConfigDict
from jist.specs.forest_spec import ForestSpec


class AttributeId(str, Enum):
    AFFECTS_VERSIONS = "versions"
    ASSIGNEE = "assignee"
    COMPONENTS = "components"
    CREATED = "created"
    CREATOR = "creator"
    CUSTOMFIELD = "customfield"
    DESCRIPTION = "description"
    DISPLAYABLE = "displayable"
    DONE = "done"
    DUEDATE = "duedate"
    EDITABLE = "editable"
    FIX_VERSIONS = "fixVersions"
    FORMULA = "expr"
    ICON = "icon"
    ISSUETYPE = "issuetype"
    ITEM = "item"
    KEY = "key"
    LABELS = "labels"
    PRIORITY = "priority"
    PROGRESS = "progress"
    PROJECT = "project"
    REPORTER = "reporter"
    STATUS = "status"
    SUM = "sum"
    SUMMARY = "summary"
    TYPE = "type"
    UNKNOWN = "unknown"
    UPDATED = "updated"
    URL = "url"
    USER = "user"
    VOTES = "votes"
    WATCHES = "watches"


class AttributeValueFormat(str, Enum):
    ANY = "any"
    BOOLEAN = "boolean"
    DURATION = "duration"
    HTML = "html"
    ID = "id"
    JSON_ARRAY = "json_array"
    JSON_OBJECT = "json"
    NUMBER = "number"
    ORDER = "order"
    TEXT = "text"
    TIME = "time"


class AttributeSpec(BaseModel):
    id: AttributeId
    format: AttributeValueFormat
    params: dict = Field(default=None)

    def __eq__(self, other):
        if not isinstance(other, AttributeSpec):
            # Don't attempt to compare against unrelated types
            return NotImplemented

        self_params_dump = json.dumps(self.params, sort_keys=True)
        other_params_dump = json.dumps(other.params, sort_keys=True)

        return (
            self.id == other.id and
            self.format == other.format and
            self_params_dump == other_params_dump
        )


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
