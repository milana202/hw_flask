import pydantic
from typing import Optional, Type

class CreateAdv(pydantic.BaseModel):
    description: str
    owner: str

    @pydantic.validator('description')
    def validate_description(cls, value):
        if len(value) < 10:
            raise ValueError('Description is too short')
        return value

class PatchAdv(pydantic.BaseModel):
    description: Optional[str]
    owner: Optional[str]

    @pydantic.validator('description')
    def validate_description(cls, value):
        if len(value) < 10:
            raise ValueError('Description is too short')
        return value

VALIDATION_CLASS = Type[CreateAdv] | Type[PatchAdv]