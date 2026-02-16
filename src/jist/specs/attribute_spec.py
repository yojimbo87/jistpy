from pydantic import BaseModel, Field, ConfigDict
from jist.specs import Version, ForestSpec, AttributeSpec


class SubscriptionWindow(BaseModel):
    forest_spec: ForestSpec = Field(alias="forestSpec")
    rows: list[int]
    attributes: list[AttributeSpec]

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class UpdateData(BaseModel):
    attribute: AttributeSpec
    values: dict
    outdated: list[int] = Field(default=None)
    empty_value_rows: list[int] = Field(default=None, alias="emptyValueRows")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class SubscriptionUpdate(BaseModel):
    id: int
    full: bool
    from_version: Version = Field(alias="fromVersion")
    version: Version
    data: list[UpdateData]
    still_loading: bool = Field(default=None, alias="stillLoading")
    inaccessible_rows: list[int] = Field(
        default=None,
        alias="inaccessibleRows"
    )
    error: dict = Field(default=None)
    attribute_errors: list[dict] = Field(default=None, alias="attributeErrors")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class SubscriptionData(BaseModel):
    id: int
    window: SubscriptionWindow
    values_upate: SubscriptionUpdate = Field(alias="valuesUpdate")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)
