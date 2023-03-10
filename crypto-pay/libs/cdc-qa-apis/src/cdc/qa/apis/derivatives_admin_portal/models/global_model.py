from enum import Enum


class GlobalSystemNameEnum(Enum):
    REFDATA_SERVICE = "REFDATA_SERVICE"
    AUTH_SERVICE = "AUTH_SERVICE"
    GLOB_SETTL_SERVICE = "GLOB_SETTL_SERVICE"


class RefDataServiceMethodEnum(Enum):
    getConfig = "getConfig"


class AuthServiceMethodEum(Enum):
    getAccountShardInfo = "getAccountShardInfo"


class GlobSettlServiceMethodEum(Enum):
    triggerGlobalSessionSettlement = "triggerGlobalSessionSettlement"
