import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestService, RailsRestApi
from cdc.qa.apis.rails.models.supermenu import SupermenuShortcutsResponse
from typing import List

logger = logging.getLogger(__name__)


class SupermenuShortcutsApi(RailsRestApi):
    """Get Supermenu Shortcuts"""

    path = "super_menu/menu_shortcuts"
    method = HttpMethods.GET
    response_type = SupermenuShortcutsResponse


class SupermenuService(RailsRestService):
    def supermenu_shortcuts(self) -> SupermenuShortcutsResponse:
        api = SupermenuShortcutsApi(host=self.host, _session=self.session)
        response = api.call()
        return SupermenuShortcutsResponse.parse_raw(b=response.content)

    def get_menu_item_keys(self) -> List[str]:
        supermenu_shortcuts_response = self.supermenu_shortcuts()
        return [menu_shortcut.menu_item_key for menu_shortcut in supermenu_shortcuts_response.menu_shortcuts]
