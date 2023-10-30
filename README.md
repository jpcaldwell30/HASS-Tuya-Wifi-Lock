# HASS-Tuya-Wifi-Lock

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This integration is an attempt to bring Tuya wifi lock compatibility to Home Assistant. It adds a lock entity to the Tuya integration. Currently, it only has support for my lock (type "jtmsbh" on the Tuya website) but I will explain how to add support for your lock below. This integration overrides the core Tuya integration. It is based on the core home assistant Tuya integeation as of commit b323295 (https://github.com/home-assistant/core/tree/b323295aa15ff6ac81e46b213a2f22440f0460de), so if you use this in the future, it might be worth cloning the repository and updating the core Tuya integration files.

## Installation instructions

- Install using [HACS](https://hacs.xyz) (Or copy the contents of `custom_components/tuya/` to `<your config dir>/custom_components/tuya/`.)

- Restart Home Assistant

- Your lock should automatically show up in the device list once you add support for your lock following the instructions below

## Usage


