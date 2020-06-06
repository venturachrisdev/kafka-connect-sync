from kafka_connect_sync.client import ConnectClient

# Mock implementation changes between python versions. Add support for both
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import patch, Mock
else:
    from mock import patch, Mock

url = 'http://kafka.com'

def test_client_constructor():
  try:
    client = ConnectClient(url=None)
  except Exception as e:
    assert str(e) == '[-] Missing required parameter: "url"'


@patch('kafka_connect_sync.client.requests.get')
def test_client_get_cluster_info(mock_get):
  mock_get.return_value.ok = True
  mock_get.return_value.json.return_value = {
      'kafka_cluster_id': 'test',
  }

  client = ConnectClient(url)
  response = client.get_cluster_info()
  assert response == {
    'kafka_cluster_id': 'test',
  }


@patch('kafka_connect_sync.client.requests.get')
def test_client_get_all(mock_get):
  connectors = [
    {
      'config': {
        'name': 'one',
        'test': 'test',
      },
    },
    {
      'config': {
          'name': 'two',
          'test': 'test',
      },
    }
  ]

  mock_get.return_value.ok = True
  mock_get.return_value.json.return_value = connectors

  client = ConnectClient(url)
  response = client.get_all()
  mock_get.assert_called_once_with('{}/connectors'.format(url))
  assert response == connectors


@patch('kafka_connect_sync.client.requests.get')
def test_client_get(mock_get):
  connector = {
    'config': {
      'name': 'one',
      'test': 'test',
    },
  }

  mock_get.return_value.ok = True
  mock_get.return_value.json.return_value = connector

  client = ConnectClient(url)
  response = client.get('one')
  assert response == connector
  mock_get.assert_called_once_with('{}/connectors/one'.format(url))


@patch('kafka_connect_sync.client.requests.delete')
def test_client_delete(mock_delete):
  mock_delete.return_value.ok = True

  client = ConnectClient(url)
  client.delete('one')
  mock_delete.assert_called_once_with('{}/connectors/one'.format(url))


@patch('kafka_connect_sync.client.requests.post')
def test_client_create(mock_create):
  connector = {
    'config': {
      'name': 'one',
      'test': 'test',
    },
  }

  expected_response = {
    'config': connector['config'],
    'name': connector['config']['name']
  }
  mock_create.return_value.ok = True

  client = ConnectClient(url)
  client.create(connector)
  mock_create.assert_called_once_with(
      '{}/connectors'.format(url), json=expected_response)


@patch('kafka_connect_sync.client.requests.put')
def test_client_update(mock_put):
  connector = {
      'config': {
          'name': 'one',
          'test': 'test',
      },
  }
  mock_put.return_value.ok = True

  client = ConnectClient(url)
  client.update(connector)
  mock_put.assert_called_once_with(
      '{}/connectors/one/config'.format(url), json=connector['config'])
