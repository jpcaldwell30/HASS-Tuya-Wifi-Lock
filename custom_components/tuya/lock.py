"""Support for Tuya Locks"""
from __future__ import annotations

from dataclasses import dataclass

import logging

from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from tuya_iot import TuyaDevice, TuyaDeviceManager

from . import HomeAssistantTuyaData
from .base import TuyaEntity
from .const import DOMAIN, TUYA_DISCOVERY_NEW, DPCode, DPType

@dataclass
class TuyaLockEntityDescription(LockEntityDescription):
    open_value: str = "True"
    closed_value: str = "False"


LOCKS: dict[str, TuyaLockEntityDescription] = {
    "jtmsbh":
        TuyaLockEntityDescription(
            key="lock_motor_state",
            icon="mdi:lock",
        ),
}

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up tuya lock dynamically through tuya discovery."""
    hass_data: HomeAssistantTuyaData = hass.data[DOMAIN][entry.entry_id]

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered tuya lock."""
        entities: list[TuyaLockEntity] = []
        for device_id in device_ids:
            device = hass_data.device_manager.device_map[device_id]
            if description := LOCKS.get(device.category):
                entities.append(TuyaLockEntity(device, hass_data.device_manager, description))

        async_add_entities(entities)

    async_discover_device([*hass_data.device_manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )

class TuyaLockEntity(TuyaEntity, LockEntity):
  """Tuya Lock Device."""

  _closed_opened_dpcode: DPCode | None = None
  entity_description: TuyaLockEntityDescription | None = None
  battery_level: int | None = None

  def __init__(
      self,
      device: TuyaDevice,
      device_manager: TuyaDeviceManager,
      description: TuyaLockEntityDescription
  ) -> None:
    """Init TuyaHaLock."""
    super().__init__(device, device_manager)

    self.entity_description = description

    # Find the DPCode for the lock state.
    if enum_type := self.find_dpcode(DPCode.M15_WIFI_01_LOCK_STATE, dptype=DPType.ENUM):
      self._closed_opened_dpcode = enum_type.dpcode

  @property
  def is_locked(self) -> bool | None:
    """Return true if the lock is locked."""
    # Get the status of the lock.
    status = self.device.status.get(self._closed_opened_dpcode)

    # If the status is None, return None.
    if status is None:
      return None

    # Return True if the status is equal to the closed_value property of the entity_description object, False otherwise.
    return status == self.entity_description.closed_value

  @property
  def battery_level(self) -> int | None:
    """Return the battery level."""
    # Get the battery level from the device status.
    battery_level = self.device.status.get(DPCode.BATTERY_PERCENTAGE)

    # If the battery level is None, return None.
    if battery_level is None:
      return None

    # Return the battery level as an integer.
    return int(battery_level)