from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, StrictStr
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from . import account, market_data, product, global_model

Model = TypeVar("Model", bound="FrozenBaseModel")


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True

    @classmethod
    def parse_raw(cls: Type[Model], b, **kwargs) -> Model:
        try:
            return super(FrozenBaseModel, cls).parse_raw(b, **kwargs)
        except ValidationError as e:
            errors = e.raw_errors
            errors.append(ErrorWrapper(ValueError(b), loc="original content:"))
            raise ValidationError(errors, model=cls) from None


class SHARD_NAMES:
    global_shard = "global00a01"
    market_data = [
        "md00a01",
    ]
    accounts = [
        "acct00a01",
        "acct01a01",
        "acct02a01",
        "acct03a01",
        "acct04a01",
        "acct05a01",
    ]
    products = [
        "product00a01",
        "product01a01",
    ]


class AdminRequestBody(FrozenBaseModel):
    """Admin Portal Request"""

    command: Union[
        account.AccountServiceMethodEnum,
        account.PositionServiceMethodEnum,
        product.ValuationNodeMethodEnum,
        market_data.ValuationNodeMethodEnum,
        global_model.RefDataServiceMethodEnum,
        global_model.AuthServiceMethodEum,
        global_model.GlobSettlServiceMethodEum,
    ] = Field(description="admin portal method")
    target: StrictStr = Field(description="Target Host IP address")
    arguments: StrictStr = Field(description="Arguments: JSON dumps format")


class AdminResponseDetail(FrozenBaseModel):
    success: bool = Field(description="success result")
    host: StrictStr = Field(description="source host ip address")
    service: Union[
        account.AccountSystemNameEnum,
        product.ProductSystemNameEnum,
        market_data.MarketDataSystemNameEnum,
        global_model.GlobalSystemNameEnum,
        global_model.AuthServiceMethodEum,
        global_model.GlobSettlServiceMethodEum,
    ] = Field(description="Admin Portal System Name")
    result: StrictStr = Field(description="response arguments result")


class AdminResponse(FrozenBaseModel):
    __root__: List[AdminResponseDetail]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class FieldProperty(FrozenBaseModel):
    name: str = Field(description="property name")
    type: Optional[str] = Field(description="property type")


class ParamOptions(FrozenBaseModel):
    __root__: Dict[str, Any]

    def __iter__(self):
        return iter(self.__root__)


class ParamProperty(FieldProperty):
    type: str = Field(description="param type")
    required: Optional[bool] = Field(description="param required")
    options: Optional[ParamOptions] = Field(description="param options")


class AdminHelpSystemCommandResponse(FrozenBaseModel):
    targets: List[str] = Field(description="command targets")
    params: Optional[List[ParamProperty]] = Field(description="param property")
    results: Optional[List[FieldProperty]] = Field(description="result property")


class AdminHelpSystemResponse(FrozenBaseModel):
    __root__: Dict[str, AdminHelpSystemCommandResponse]

    def items(self):
        return self.__root__.items()

    def get(self, key, default=None):
        return self.__root__.get(key, default)


class AdminHelpResponse(FrozenBaseModel):
    __root__: Dict[str, AdminHelpSystemResponse]

    def items(self):
        return self.__root__.items()

    def get(self, key, default=None):
        return self.__root__.get(key, default)


class InstrumentInfo(FrozenBaseModel):
    instId: int = Field(description="instrument id")
    symbol: str = Field(description="instrument symbol id")


class AdminHelpPlaceholderRequestParams(FrozenBaseModel):
    key: str = Field(description="e.g. ALL_TRADABLE_INSTRUMENTS")


class AdminHelpPlaceholderResponse(FrozenBaseModel):
    __root__: List[InstrumentInfo]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
