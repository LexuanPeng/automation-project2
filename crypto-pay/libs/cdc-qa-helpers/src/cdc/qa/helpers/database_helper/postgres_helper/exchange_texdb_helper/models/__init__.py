import json
from decimal import Decimal
from functools import partial
from typing import Type, TypeVar

from pydantic import BaseModel
from pydantic.error_wrappers import ErrorWrapper, ValidationError

Model = TypeVar("Model", bound="FrozenBaseModel")


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True
        json_loads = partial(json.loads, parse_float=Decimal)

    @classmethod
    def parse_obj(cls: Type[Model], b, **kwargs) -> Model:
        try:
            return super(FrozenBaseModel, cls).parse_obj(b, **kwargs)
        except ValidationError as e:
            errors = e.raw_errors
            errors.append(ErrorWrapper(ValueError(b), loc="original content:"))
            raise ValidationError(errors, model=cls) from None
