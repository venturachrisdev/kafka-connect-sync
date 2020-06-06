from kafkaconnectsync import sync

# Mock implementation changes between python versions. Add support for both
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import patch, Mock
else:
    from mock import patch, Mock

url = 'http://kafka.com'

""" Throws if no url paramater is provided """
def test_sync():
  try:
    sync(url=None, connectors=None)
  except Exception as e:
    assert str(e) == '[-] Missing required parameter: "url"'

""" Avoid calling API if no connectors are provided """
@patch('kafkaconnectsync.client.requests.get')
def test_sync_null_connectors(mock_get):
  sync(url)
  sync(url, connectors=None)
  mock_get.assert_not_called()
