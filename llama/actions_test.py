

from llama import actions


def test_message_error_action_creators():

    # Error Result
    action = actions.message_decode_error_result("foo",
                                                 "bar",
                                                 "err")

    assert action["type"] == actions.MESSAGE_DECODE_ERROR_RESULT

    # Decode Error
    action = actions.message_decode_error("foo", "bar", 23)

    assert action["type"] == actions.MESSAGE_DECODE_ERROR
    assert type(action["payload"]["error"]) == str


