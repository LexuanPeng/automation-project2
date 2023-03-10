from typing import List

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel
from pydantic import Field


# --------------------------------- SupermenuShortcuts --------------------------------- #
class SupermenuShortcutsResponse(RailsResponse):
    class MenuShortcuts(FrozenBaseModel):
        position: int
        menu_item_key: str

    menu_shortcuts: List[MenuShortcuts] = Field()
