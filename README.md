# llama

An opinionated library for writing services on a MQTT message bus.


## Why?


Something along the lines of: After implementing [DaliQTT](https://github.com/cccb/daliqtt)
I wanted something more generalized to create new services more
easily.

Also see [Alpaca](https://github.com/cameliot/alpaca), the Go implementation
of this library.

## How to use

Creating a new service in your network
is now as easy as:

```python

# Connect to MQTT broker and start dispatch loop
dispatch, receive = mqtt.connect("localhost:1883", {
    "strings": "v1/simple/strings",
})

handle(dispatch, receive())

```

With a handler like

```python
def handle(dispatch, actions):
    """Process incoming actions"""

    for action in actions:
        if action["type"] == REVERSE_REQUEST:
            dispatch(_handle_reverse(action["payload"]))

```

The `receive` function can be used in a blocking and non-blocking
fashion by passing a `timeout` in seconds (e.g. `receive(timeout=0.25)`
and it can be used in a one shot kind of way, by passing `once=True`.

This way `receive(once=True)` will block until an action is received,
or (if specified) the `timeout` will occure.


### Error handling

In case decoding the MQTT payload failed, an `llama.actions.MESSAGE_DECODE_ERROR_RESULT`
is received.

### Example

For a simple working example please checkout the [examples/reverser/reverser.py](https://github.com/cameliot/llama/blob/master/examples/reverser/reverser.py) string reversal service.


