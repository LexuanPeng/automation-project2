from enum import Enum


class AccountSystemNameEnum(Enum):
    ACCOUNT_SERVICE = "ACCOUNT_SERVICE"
    POSITION_SERVICE = "POSITION_SERVICE"
    POSITION_SERVICE0 = "POSITION_SERVICE0"
    POSITION_SERVICE1 = "POSITION_SERVICE1"
    POSITION_SERVICE2 = "POSITION_SERVICE2"
    POSITION_SERVICE3 = "POSITION_SERVICE3"
    POSITION_SERVICE4 = "POSITION_SERVICE4"
    POSITION_SERVICE5 = "POSITION_SERVICE5"
    POSITION_SERVICE6 = "POSITION_SERVICE6"
    POSITION_SERVICE7 = "POSITION_SERVICE7"


# --- VALUATION_NODE ----
class AccountServiceMethodEnum(Enum):
    getUserAccountDetails = "getUserAccountDetails"
    reloadAccountData = "reloadAccountData"
    status = "status"


# --- POSITION_SERVICE ----
class PositionServiceMethodEnum(Enum):
    applyJournal = "applyJournal"
