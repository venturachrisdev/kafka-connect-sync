from kafka_connect_sync import sync

# Mock implementation changes between python versions. Add support for both
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import patch, Mock
else:
    from mock import patch, Mock

url = 'http://kafka.com'

def test_sync():
  try:
    sync(url=None, connectors=None)
  except Exception as e:
    assert str(e) == '[-] Missing required parameter: "url"'

@patch('kafka_connect_sync.client.requests.get')
def test_sync_null_connectors(mock_get):
  sync(url)
  sync(url, connectors=None)
