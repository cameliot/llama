
import time
import queue
import json
import logging
import functools

import paho.mqtt.client as paho_mqtt

import llama.actions as llama_actions


class MessageError(Exception):
    pass


class MessageDecodeError(MessageError):
    pass


def _encode_action_type(routes, action_type):
    """
    Encode the outbound action type, apply routing and
    create MQTT topic.

    :param routes: The routing dict
    :type routes: dict

    :param action_type: The type of action
    :type action_type: str

    :returns: The routed MQTT topic
    """
    return ""


def _decode_action_type(routes, topic):
    """
    Decode an inbound MQTT topic into an action type.

    :param routes: The routing dict
    :type routes: dict

    :param topic: The MQTT topic
    :type topic: str

    :returns: The action type
    """
    return ""


def _decode_action(routes, topic, payload):
    """
    Decode an incoming message into an action

    :param topic: The MQTT topic
    :type topic: str

    :param payload: The message body
    :type payload: bytes

    :returns: An action
    """
    try:
        action_payload = json.loads(msg.payload)
    except Exception(e):
        raise MessageDecodeError(str(e))

    # Apply routing to topic
    action_type = _decode_action_type(routes, msg.topic)

    # Create action
    action = {
        "type": action_type,
        "payload": action_payload,
    }

    return action


def _on_message(messages, _client, _obj, msg):
    """
    Handle incoming messages from MQTT

    :param messages: A message queue for pushing incoming raw messages.
    :type messages: queue.Queue

    :param _client: The paho MQTT client (unrequired)
    :type _client: paho.mqtt.client.Client

    :param msg: The incoming MQTT message.
    :type msg: paho.mqtt.client.MqttMessage
    """
    logging.debug("Incoming MQTT message: {}".format(msg))
    actions.put(msg)


def _receive(messages, routes, timeout=None):
    """
    General receive function

    :param actions: Incoming actions
    :type actions: queue.Queue

    :param timeout: Set a timeout to make it non blocking
    :type timeout: int | None

    :returns: The action or None if queue empty an non blocking
    """
    try:
        msg = messages.get(timeout)
        topic = msg.topic
        payload = msg.payload

        # Decode messages into action
        return _decode_action(routes, topic, payload)

    except queue.Empty:
        return None

    except MessageDecodeError as e:
        logging.warning("Could not decode incoming message: {}".format(e))

        return llama_actions.message_decode_error_result(topic, payload, e)


def _dispatch(client, routes, action):
    """
    General action dispatch function

    Dispatches an action to MQTT. Creates topic from
    Action Type by applying the routing.

    :param client: The MQTT client
    :type client: paho.mqtt.client.Client

    :param routes: The routing dict, see connect(address, routes)
    :type routes: dict

    :param action: An action
    :type action: dict
    """
    try:
        payload = json.dumps(action.get("payload")).encode("utf-8")
    except Exception as e:
        logging.error("Could not encode payload: {}".format(e))
        return

    topic = _encode_topic(routes, action.get("type"))

    ticket = client.publish(topic, payload)
    ticket.wait_for_publish()


def connect(address, routes):
    """
    Open connection, subscribe and create dispatch

    :param address: The MQTT broker address (host:port)
    :type address: str

    :param routes: The routes mapping. In actions the @prefix
                   will translate into a route handle and expanded
                   to the full topic.

                   e.g. @lights/SET_VALUE_REQUEST

                   will yield a MQTT topic

                        v1/upstairs/lights/SET_VALUE_REQUEST

                   and vice versa on receive.
    :type routes: dict

    :returns: The receive and dispatch functions
    :type returns: tuple of function
    """
    try:
        host, port = address.split(":", 1)
    except ValueError:
        host = address
        port = 1883

    logging.info("Connecting to mqtt://{}:{}".format(host, port))

    messages_queue = queue.Queue()

    client = paho_mqtt.Client()

    # Configure Client
    client.reconnect_delay_set(min_delay=1, max_delay=15)

    # Client Callbacks
    client.on_log = _log
    client.on_message = functools.partial(_on_message, messages_queue)
    client.on_connect = functools.partial(_on_connect, base_topic)
    client.on_disconnect = _on_disconnect

    # Open connection
    client.connect(host, int(port), 60)
    logging.info("MQTT connected.")

    # Start client in dedicated thread. Do not
    # block our main application.
    client.loop_start()

    # Make receive function
    receive = functools.partial(_receive, messages_queue, routes)

    # Create dispatch function
    dispatch = functools.partial(_dispatch, client, routes)

    return receive, dispatch

