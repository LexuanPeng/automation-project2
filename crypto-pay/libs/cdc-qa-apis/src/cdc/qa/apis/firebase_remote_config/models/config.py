from datetime import datetime
from typing import Optional, Dict, List

from pydantic import Field

from cdc.qa.apis.firebase_remote_config.models import FrozenBaseModel


class Value(FrozenBaseModel):
    value: str


class RemoteConfigGetResponse(FrozenBaseModel):
    class Condition(FrozenBaseModel):
        name: str
        expression: str
        tagColor: str

    class Parameter(FrozenBaseModel):
        defaultValue: Value
        conditionalValues: Optional[Dict[str, Value]]
        valueType: str

    class Version(FrozenBaseModel):
        class UpdateUser(FrozenBaseModel):
            email: str

        versionNumber: str
        updateTime: datetime
        updateUser: UpdateUser
        updateOrigin: str
        updateType: str

    conditions: List[Condition] = Field()
    parameters: Dict[str, Parameter] = Field()
    version: Version = Field()
