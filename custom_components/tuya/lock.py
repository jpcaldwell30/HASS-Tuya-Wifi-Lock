# """Support for Tuya Locks"""
# from __future__ import annotations
# from dataclasses import dataclass
# import logging
# from typing import Any

# from homeassistant.const import PERCENTAGE
# from homeassistant.components.lock import LockEntity, LockEntityDescription
# from homeassistant.components.sensor import (
#     SensorDeviceClass,
#     SensorEntity,
# )
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant, callback
# from homeassistant.helpers.dispatcher import async_dispatcher_connect
# from homeassistant.helpers.entity_platform import AddEntitiesCallback
# from tuya_iot import TuyaDevice, TuyaDeviceManager


# _LOGGER = logging.getLogger(__name__)

# from . import HomeAssistantTuyaData
# from .base import TuyaEntity
# from .const import DOMAIN, TUYA_DISCOVERY_NEW, DPCode

# @dataclass
# class TuyaLockEntityDescription(LockEntityDescription):
#     open_value: bool = "True"
#     closed_value: str = "False"

#     @property
#     def unique_id(self) -> str:
#         """Return the unique ID of the entity."""
#         return self.device_id

# LOCKS: dict[str, TuyaLockEntityDescription] = {
#     "jtmsbh":
#         TuyaLockEntityDescription(
#             key="lock_motor_state",
#             icon="mdi:lock",
#         ),
# }

# async def async_setup_entry(
#         hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
# ) -> None:
#     """Set up tuya lock dynamically through tuya discovery."""
#     hass_data: HomeAssistantTuyaData = hass.data[DOMAIN][entry.entry_id]

#     @callback
#     def async_discover_device(device_ids: list[str]) -> None:
#         """Discover and add a discovered tuya lock."""
#         entities: list[TuyaLockEntity] = []
#         for device_id in device_ids:
#             device = hass_data.device_manager.device_map[device_id]
#             if description := LOCKS.get(device.category):
#                 entities.append(TuyaLockBatterySensor(device, hass_data.device_manager))
#                 entities.append(TuyaLockEntity(device, hass_data.device_manager, description))

#         async_add_entities(entities)

#     async_discover_device([*hass_data.device_manager.device_map])

#     entry.async_on_unload(
#         async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
#     )

# class TuyaLockEntity(TuyaEntity, LockEntity):
#   """Tuya Lock Device."""

#   _closed_opened_dpcode: DPCode | None = None
#   entity_description: TuyaLockEntityDescription | None = None
#   battery_level: int | None = None

#   def __init__(
#       self,
#       device: TuyaDevice,
#       device_manager: TuyaDeviceManager,
#       description: TuyaLockEntityDescription
#   ) -> None:
#     """Init TuyaHaLock."""
#     super().__init__(device, device_manager)

#     self.entity_description = description
#     self._closed_opened_dpcode = DPCode.M15_WIFI_01_LOCK_STATE

#   @property
#   def is_locked(self) -> bool | None:
#     """Return true if the lock is locked."""
#     # Get the status of the lock.
#     _LOGGER.debug("closed open dpcode is %s", self._closed_opened_dpcode)
#     status = self.device.status.get(self._closed_opened_dpcode)
#     _LOGGER.debug("status is %s", status)

#     # If the status is None, return None.
#     if status is None:
#       return None

#     # Return True if the status is equal to the closed_value property of the entity_description object, False otherwise.
#     return status == self.entity_description.closed_value
  
#   @property
#   def extra_state_attributes(self) -> dict[str, Any]:
#     """Return the device specific state attributes."""
#     """Return the battery level."""
#     # Get the battery level from the device status.
#     battery_level = self.device.status.get(DPCode.M15_WIFI_01_BATTERY_PERCENTAGE)
#     _LOGGER.debug("battery level is %s", battery_level)
#     # If the battery level is None, return None.
#     if battery_level is None:
#       return None

#     # Return the battery level as an integer.
#     return {
#           "battery_percentage": int(battery_level)
#     }
  
#   def lock(self, **kwargs):
#     """Lock the lock."""
#     self._send_command([{"code": self.entity_description.key, "value": self.entity_description.closed_value}])

#   def unlock(self, **kwargs):
#     """Unlock the lock."""
#     self._send_command([{"code": self.entity_description.key, "value": self.entity_description.open_value}])


# class TuyaLockBatterySensor(SensorEntity, TuyaEntity):
#     _attr_device_class = SensorDeviceClass.BATTERY
#     _attr_native_unit_of_measurement = PERCENTAGE
#     _attr_name: str | None = None
#     battery_level: int | None = None

#     """Tuya lock battery sensor."""
#     def __init__(self, device: TuyaDevice, device_manager: TuyaDeviceManager):
#         """Initialize the sensor."""
#         super().__init__(device, device_manager)

#         self._attr_name = "Lock Battery"
#         self.dpcode = DPCode.M15_WIFI_01_BATTERY_PERCENTAGE

#     @property
#     def state(self):
#         """Return the state of the sensor."""
#         return self.battery_level

#     def update(self):
#         """Update the battery level."""
#         battery_level = int(self.device.status.get(self.dpcode))
#         if battery_level is None:
#             return 
#         self.battery_level = battery_level


# """Support for Tuya Locks"""
# from __future__ import annotations
# from dataclasses import dataclass
# import logging
# from typing import Any

# from homeassistant.const import PERCENTAGE
# from homeassistant.components.lock import LockEntity, LockEntityDescription
# from homeassistant.components.sensor import (
#     SensorDeviceClass,
#     SensorEntity,
#     SensorEntityDescription
# )
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant, callback
# from homeassistant.helpers.dispatcher import async_dispatcher_connect
# from homeassistant.helpers.entity_platform import AddEntitiesCallback
# from tuya_iot import TuyaDevice, TuyaDeviceManager

# _LOGGER = logging.getLogger(__name__)

# from . import HomeAssistantTuyaData
# from .base import TuyaEntity
# from .const import DOMAIN, TUYA_DISCOVERY_NEW, DPCode

# @dataclass
# class TuyaLockEntityDescription(LockEntityDescription):
#     open_value: bool = True
#     closed_value: bool = False
    
#     @property
#     def unique_id(self) -> str:
#         """Return the unique ID of the entity."""
#         return self.device_id

# @dataclass        
# class TuyaLockBatterySensorDescription(SensorEntityDescription):
#     _attr_device_class = SensorDeviceClass.BATTERY
#     _attr_native_unit_of_measurement = PERCENTAGE

#     @property
#     def unique_id(self) -> str:
#         """Return the unique ID of the entity."""
#         return f"{self.device_id}_battery"

# LOCKS: dict[str, TuyaLockEntityDescription] = {
#     "jtmsbh":
#         TuyaLockEntityDescription(
#             key=DPCode.M15_WIFI_01_LOCK_STATE,
#             icon="mdi:lock"
#         )
# }

# _LOGGER = logging.getLogger(__name__)

# async def async_setup_entry(
#         hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
# ) -> None:
#     """Set up tuya lock dynamically through tuya discovery."""
#     hass_data: HomeAssistantTuyaData = hass.data[DOMAIN][entry.entry_id]

#     @callback
#     def async_discover_device(device_ids: list[str]) -> None:
#         """Discover and add a discovered tuya lock."""
#         entities: list[TuyaLockEntity] = []
#         for device_id in device_ids:
#             device = hass_data.device_manager.device_map[device_id]
#             if description := LOCKS.get(device.category):
#                 entities.append(TuyaLockBatterySensor(device, hass_data.device_manager, TuyaLockBatterySensorDescription(key=DPCode.M15_WIFI_01_LOCK_STATE)))
#                 entities.append(TuyaLockEntity(device, hass_data.device_manager, description))
                
#         async_add_entities(entities)

#     async_discover_device([*hass_data.device_manager.device_map])

#     entry.async_on_unload(
#         async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
#     )

# class TuyaLockEntity(TuyaEntity, LockEntity):
#   """Tuya Lock Device."""
#   _closed_opened_dpcode: DPCode | None = None
#   entity_description: TuyaLockEntityDescription | None = None
#   battery_level: int | None = None

#   def __init__(
#       self,
#       device: TuyaDevice,
#       device_manager: TuyaDeviceManager,
#       description: TuyaLockEntityDescription
#   ) -> None:
#     """Init TuyaHaLock."""
#     super().__init__(device, device_manager)

#     self.entity_description = description

#     # Find the DPCode for the lock state.
#     self._closed_opened_dpcode = self.entity_description.key

#   @property
#   def is_locked(self) -> bool | None:
#     """Return true if the lock is locked."""
#     # Get the status of the lock.
#     _LOGGER.debug("closed open dpcode is %s", self._closed_opened_dpcode)
#     status = self.device.status.get(self._closed_opened_dpcode)
#     _LOGGER.debug("status is %s", status)

#     # If the status is None, return None.
#     if status is None:
#       return None

#     # Return True if the status is equal to the closed_value property of the entity_description object, False otherwise.
#     return status == self.entity_description.closed_value
    
#   @property
#   def extra_state_attributes(self) -> dict[str, Any]:
#     """Return the device specific state attributes."""
#     """Return the battery level."""
#     # Get the battery level from the device status.
#     battery_level = self.device.status.get(DPCode.M15_WIFI_01_BATTERY_PERCENTAGE)
#     _LOGGER.debug("battery level is %s", battery_level)
#     # If the battery level is None, return None.
#     if battery_level is None:
#       return None

#     # Return the battery level as an integer.
#     return {
#           "battery_percentage": int(battery_level)
#     }

#   def lock(self, **kwargs):
#     """Lock the lock."""
#     self._send_command([{"code": self.entity_description.key, "value": self.entity_description.closed_value}])

#   def unlock(self, **kwargs):
#     """Unlock the lock."""
#     self._send_command([{"code": self.entity_description.key, "value": self.entity_description.open_value}])
    
# class TuyaLockBatterySensor(SensorEntity, TuyaEntity):
#     entity_description: TuyaLockBatterySensorDescription | None = None
#     battery_level: int | None = None

#     """Tuya lock battery sensor."""
#     def __init__(self, 
#       device: TuyaDevice, 
#       device_manager: TuyaDeviceManager, 
#       description: TuyaLockBatterySensorDescription
#     ) -> None:
#       """Initialize the sensor."""
#       super().__init__(device, device_manager)

#     entity_description = description

#     @property
#     def state(self):
#         """Return the state of the sensor."""
#         return self.battery_level

#     def update(self):
#         """Update the battery level."""
#         battery_level = int(self.device.status.get(self.entity_description.key))
#         if battery_level is None:
#             return 
#         self.battery_level = battery_level

"""Support for Tuya Locks"""
from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.const import PERCENTAGE
from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from tuya_iot import TuyaDevice, TuyaDeviceManager


_LOGGER = logging.getLogger(__name__)

from . import HomeAssistantTuyaData
from .base import TuyaEntity
from .const import DOMAIN, TUYA_DISCOVERY_NEW, DPCode

@dataclass
class TuyaLockEntityDescription(LockEntityDescription):
    open_value: bool = True
    closed_value: bool = False

LOCKS: dict[str, TuyaLockEntityDescription] = {
    "jtmsbh":
        TuyaLockEntityDescription(
            key=DPCode.M15_WIFI_01_LOCK_STATE,
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
    self._closed_opened_dpcode = DPCode.M15_WIFI_01_LOCK_STATE

  @property
  def is_locked(self) -> bool | None:
    """Return true if the lock is locked."""
    # Get the status of the lock.
    _LOGGER.debug("closed open dpcode is %s", self._closed_opened_dpcode)
    status = self.device.status.get(self._closed_opened_dpcode)
    _LOGGER.debug("status is %s", status)

    # If the status is None, return None.
    if status is None:
      return None

    # Return True if the status is equal to the closed_value property of the entity_description object, False otherwise.
    return status == self.entity_description.closed_value

  def lock(self, **kwargs):
    """Lock the lock."""
    self._send_command([{"code": self.entity_description.key, "value": self.entity_description.closed_value}])

  def unlock(self, **kwargs):
    """Unlock the lock."""
    self._send_command([{"code": self.entity_description.key, "value": self.entity_description.open_value}])






# class TuyaLockBatterySensor(SensorEntity, TuyaEntity):
#     _attr_device_class = SensorDeviceClass.BATTERY
#     _attr_native_unit_of_measurement = PERCENTAGE
#     battery_level: int | None = None

#     """Tuya lock battery sensor."""
#     def __init__(self, 
#       device: TuyaDevice, 
#       device_manager: TuyaDeviceManager
#       ) -> None:
#         """Initialize the sensor."""
#         super().__init__(device, device_manager)
#         #_attr_unique_id =  f"{device.id}_battery"
#         #self._attr_name = "Lock Battery"
#         self.dpcode = DPCode.M15_WIFI_01_BATTERY_PERCENTAGE

#     @property
#     def state(self):
#       """Return the state of the sensor."""
#       return self.battery_level

#     def update(self):
#       """Update the battery level."""
#       # battery_level = int(self.device.status.get(self.dpcode))
#       battery_level = int(999)
#       if battery_level is None:
#           return 
#       self.battery_level = battery_level