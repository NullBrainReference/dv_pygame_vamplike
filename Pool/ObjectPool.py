from typing import Protocol
from typing import TypeVar, Generic

    
class IPoolable(Protocol):
    @property
    def is_active(self) -> bool:
        pass

    def release(self):
        pass

    def occupy(self):
        pass

T = TypeVar('T', bound=IPoolable)

class ObjectPool(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def add(self, item: T):
        self.items.append(item)

    def get_free(self) -> T | None:
        for item in self.items:
            if item.is_active == False:
                return item
        return None
