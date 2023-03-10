from typing import List

from pydantic import Field

from . import FrozenBaseModel


class SysConfigDetail(FrozenBaseModel):
    key: str = Field()
    value: str = Field()


class SysConfigList(FrozenBaseModel):
    __root__: List[SysConfigDetail] = Field(description="Sys Config List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
