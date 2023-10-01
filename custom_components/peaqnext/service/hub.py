import logging
import time
from typing import Any
from datetime import datetime

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change

_LOGGER = logging.getLogger(__name__)


class Hub:
    hub_id = 33512
    hubname = "PeaqOffpeak"    
    
    def __init__(self, hass) -> Any:        
        self.state_machine: HomeAssistant = hass        
        async_track_state_change(
            self.state_machine,
            [self.spotprice.entity],
            self.async_state_changed,
        )

    @callback
    async def async_state_changed(self, entity_id, old_state, new_state):
        if entity_id is not None:
            try:
                if old_state is None or old_state != new_state:
                    await self.spotprice.async_update_spotprice()
            except Exception as e:
                msg = f"Unable to handle data-update: {entity_id} {old_state}|{new_state}. Exception: {e}"
                _LOGGER.error(msg)
