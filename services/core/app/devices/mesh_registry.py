from pydantic import BaseModel, Field
import datetime

class RegisteredDevice(BaseModel):
    device_id: str
    user_id: str
    name: str
    platform: str
    is_active: bool = True
    paired_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    last_seen_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class DeviceMeshRegistry:
    def __init__(self):
        self._devices: dict[str, RegisteredDevice] = {}

    def pair_device(self, user_id: str, device_id: str, name: str, platform: str) -> RegisteredDevice:
        device = RegisteredDevice(device_id=device_id, user_id=user_id, name=name, platform=platform, is_active=True)
        self._devices[device_id] = device
        return device

    def revoke_device(self, device_id: str) -> bool:
        """Instantly revoke device authorization and kill access."""
        if device_id in self._devices:
            self._devices[device_id].is_active = False
            return True
        return False

    def is_device_authorized(self, device_id: str) -> bool:
        device = self._devices.get(device_id)
        return device is not None and device.is_active

    def get_user_devices(self, user_id: str) -> list[RegisteredDevice]:
        return [d for d in self._devices.values() if d.user_id == user_id and d.is_active]

device_mesh = DeviceMeshRegistry()

