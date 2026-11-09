from pydantic import BaseModel, Field
import datetime

class MemoryItem(BaseModel):
    id: str
    key: str
    value: str
    user_approved: bool = True
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class MemoryStore:
    def __init__(self):
        self._memories: dict[str, MemoryItem] = {}

    def set_memory(self, key: str, value: str, user_approved: bool = True) -> MemoryItem:
        if not user_approved:
            raise ValueError("Memories cannot be stored without explicit user approval.")
        item = MemoryItem(id=f"mem-{len(self._memories)+1}", key=key, value=value, user_approved=True)
        self._memories[key] = item
        return item

    def get_memory(self, key: str) -> MemoryItem | None:
        return self._memories.get(key)

    def list_memories(self) -> list[MemoryItem]:
        return list(self._memories.values())

    def delete_memory(self, key: str) -> bool:
        if key in self._memories:
            del self._memories[key]
            return True
        return False

memory_store = MemoryStore()

