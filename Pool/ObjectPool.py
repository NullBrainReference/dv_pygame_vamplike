from typing import Protocol
from typing import TypeVar, Generic
from collections import deque

    
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
        self.free: deque[T] = deque()

    def add(self, item: T):
        self.items.append(item)
        if not item.is_active:
            self.free.append(item)

    def get_free(self) -> T | None:
        #Todo: remove log msg
        print(f"pool has {len(self.free)} items. (remove this log!)")
        if self.free:
            obj = self.free.pop()
            obj.occupy()
            return obj
        return None

    def release(self, item: T):
        item.release()
        self.free.append(item)


