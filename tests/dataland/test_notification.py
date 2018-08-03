import pytest
import responses

class TestMailgunNotification(object):

    @responses.activate
    def test_notify_send_email_with_correct_params(self):
        assert True # still have to figure out how to mock http
