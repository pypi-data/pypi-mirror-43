# aioevent
A simple library that enables easier asynchronous event handling in python.

## Features

### Optional event propagation
`EventEmitter` classes can proxy events from other event emitters to enable
hierarchical event propagation (e.g. a `ContentBox` element can forward events
from a `Button` element to allow for a `click` listener on the `ContextBox`).

### Inline event listeners
Easily create inline event listeners.
```python
@event_listener(emitter, EventType)
async def my_event_subscription(event):
    print(f"Got event {repr(event)} (emitted by {repr(event.target)}).")
    # Do something interesting with the event.
    await db.record_event(event)

# Do some things
my_event_subscription.unsubscribe()
```
