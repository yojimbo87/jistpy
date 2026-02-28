from pydantic import BaseModel, Field, ConfigDict


class PatRequest(BaseModel):
    name: str
    expiration_duration: int = Field(alias="expirationDuration")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


# {\"id\":102,\"name\":\"jistpy-f242429a5b314b00b82c541de0960855\",\"createdAt\":\"2026-02-26T22:42:21.247+00:00\",\"expiringAt\":\"2026-02-27T22:42:21.247+00:00\",\"rawToken\":\"MjUxNzA1MzE5ODQxOj7Ta/HGo+MaFskVU5bff4Lf37LQ\"}
class PatResponse(BaseModel):
    id: int
    name: str
    created_at: str = Field(alias="createdAt")
    expiring_at: str = Field(alias="expiringAt")
    raw_token: str = Field(alias="rawToken")
