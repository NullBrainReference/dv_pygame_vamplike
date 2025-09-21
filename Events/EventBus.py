class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        self._listeners.setdefault(event_type, []).append(callback)

    def emit(self, event):
        for cb in self._listeners.get(type(event), []):
            cb(event)


bus = EventBus()
