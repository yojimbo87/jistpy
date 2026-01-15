from pydantic import BaseModel, Field

class Structure(BaseModel):
    id: int
    name: str = Field(alias = "name")
    description: str