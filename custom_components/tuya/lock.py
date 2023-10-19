"""Support for Tuya wifi lock platform."""
from __future__ import annotations

from typing import Any

from tuya_iot import TuyaDevice, TuyaDeviceManager

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomeAssistantTuyaData
from .base import TuyaEntity
from .const import DOMAIN, TUYA_DISCOVERY_NEW, DPCode

from homeassistant.components.lock import (
    LockDeviceClass,
    LockEntity,
    LockEntityDescription,
    LockEntityFeature
)

LOCKS: dict[str, tuple[LockEntityDescription, ...]] = {
    "jtmsbh": (
        LockEntityDescription(
            key="lock_motor_state",
            icon="mdi:lock",
        )
    ),
}

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up tuya sensors dynamically through tuya discovery."""
    hass_data: HomeAssistantTuyaData = hass.data[DOMAIN][entry.entry_id]

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered tuya lock."""
        entities: list[TuyaLockEntity] = []
        for device_id in device_ids:
            device = hass_data.device_manager.device_map[device_id]
            if descriptions := LOCKS.get(device.category):
                for description in descriptions:
                    if description.key in device.status:
                        entities.append(
                            TuyaLockEntity(
                                device, hass_data.device_manager, description
                            )
                        )

        async_add_entities(entities)

    async_discover_device([*hass_data.device_manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


class TuyaLockEntity(TuyaEntity, LockEntity):
    """Tuya Lock Device."""

    def __init__(
        self,
        device: TuyaDevice,
        device_manager: TuyaDeviceManager,
        description: LockEntityDescription,
    ) -> None:
        """Init TuyaHaLock."""
        super().__init__(device, device_manager)
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    @property
    def is_locked(self) -> bool:
        """Return true if lock is on."""
        return self.device.status.get(self.entity_description.key, False)

    def lock(self, **kwargs):
        """Lock the lock."""
        self._send_command([{"code": self.entity_description.key, "value": True}]) #tuya  method

    def unlock(self, **kwargs):
        """Unlock the lock."""
        self._send_command([{"code": self.entity_description.key, "value": False}]) #tuya  method
