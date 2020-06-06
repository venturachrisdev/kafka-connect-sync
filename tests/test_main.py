""" Main module tests """

# Mock implementation changes between python versions. Add support for both
from kafkaconnectsync import sync
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import patch, Mock
else:
    from mock import patch, Mock

URL = 'https://kafka.com'


def test_sync():
    """ it should throw an error if no url is provided """
    try:
        sync(url=None, connectors=None)
    except RuntimeError as err:
        assert str(err) == '[-] Missing required parameter: "url"'


@patch('kafkaconnectsync.client.requests.get')
def test_sync_null_connectors(mock_get):
    """ it should avoid calling API if no connectors are provided """

    sync(url=URL, connectors=[])
    sync(url=URL, connectors=None)
    mock_get.assert_not_called()
