from pydantic import BaseModel, Field, ConfigDict


class PatRequest(BaseModel):
    name: str
    expiration_duration: int = Field(alias="expirationDuration")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class PatResponse(BaseModel):
    token_name: str
    # TODO: token contains json object which should be parsed into fields
    token: str
