
import queue

import paho.mqtt.client as paho_mqtt

from llama import mqtt


def _make_msg(topic, payload):
    """Create message helper"""
    if type(payload) != bytes:
        payload = bytes(payload, "utf-8")

    msg = paho_mqtt.MQTTMessage(topic=topic)
    msg.payload=payload

    return msg



def test_decode_action_type():

    expected = {
		"foo/BAR": "foo/BAR",
		"v1/bar/FNORD": "@bar/FNORD",
		"@bar/FOO": "@bar/FOO",
		"v1/basement/foo/FNORD": "@foo/FNORD",
    }

    routes = {
        "foo": "v1/basement/foo",
        "bar": "v1/bar",
    }

    for topic, result in expected.items():
        decoded = mqtt._decode_action_type(routes, topic)
        assert decoded == result



def test_encode_action_type():
    routes = {
		"foo": "v1/basement/foo",
		"bar": "v1/bar",
	}

    expected = {
		"foo/BAR": "foo/BAR",
		"@foo/BAR": "v1/basement/foo/BAR",
		"@bar/FOO": "v1/bar/FOO",
		"@bar": "@bar",
	}

    for action_type, result in expected.items():
        topic = mqtt._encode_action_type(routes, action_type)
        assert topic == result




