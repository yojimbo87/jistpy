from pydantic import BaseModel, Field

class Structure(BaseModel):
    id: int
    whoa: str = Field(alias = "name")
    description: str