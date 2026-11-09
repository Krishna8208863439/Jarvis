import pytest
from app.devices.mesh_registry import device_mesh

def test_device_pairing_and_authorization():
    dev = device_mesh.pair_device(user_id="user-123", device_id="desktop-win", name="My Windows PC", platform="windows")
    assert dev.is_active is True
    assert device_mesh.is_device_authorized("desktop-win") is True

    # Pair second device
    dev_phone = device_mesh.pair_device(user_id="user-123", device_id="pixel-phone", name="Pixel 8 Pro", platform="android")
    active_devices = device_mesh.get_user_devices("user-123")
    assert len(active_devices) == 2

def test_device_revocation_instant_kill():
    # Revoke phone
    revoked = device_mesh.revoke_device("pixel-phone")
    assert revoked is True
    assert device_mesh.is_device_authorized("pixel-phone") is False

    active_devices = device_mesh.get_user_devices("user-123")
    assert len(active_devices) == 1
    assert active_devices[0].device_id == "desktop-win"

