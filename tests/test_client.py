""" ConnectClient tests """
from kafkaconnectsync.client import ConnectClient

# Mock implementation changes between python versions. Add support for both
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import patch, Mock
else:
    from mock import patch, Mock

URL = 'https://kafka.com'


def test_client_constructor():
    """ it should throw if no url is provided """
    try:
        client = ConnectClient(url=None)
        client.get_all()
    except RuntimeError as err:
        assert str(err) == '[-] Missing required parameter: "url"'


@patch('kafkaconnectsync.client.requests.get')
def test_client_get_cluster_info(mock_get):
    """ it should get cluster info from API """
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        'kafka_cluster_id': 'test',
    }

    client = ConnectClient(url=URL)
    response = client.get_cluster_info()
    assert response == {
        'kafka_cluster_id': 'test',
    }


@patch('kafkaconnectsync.client.requests.get')
def test_client_get_all(mock_get):
    """ it should get all exiting connectors from API """
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

    client = ConnectClient(url=URL)
    response = client.get_all()
    mock_get.assert_called_once_with('{}/connectors'.format(URL))
    assert response == connectors


@patch('kafkaconnectsync.client.requests.get')
def test_client_get(mock_get):
    """ it should get a single connector by ID """
    connector = {
        'config': {
            'name': 'one',
            'test': 'test',
        },
    }

    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = connector

    client = ConnectClient(url=URL)
    response = client.get('one')
    assert response == connector
    mock_get.assert_called_once_with('{}/connectors/one'.format(URL))


@patch('kafkaconnectsync.client.requests.delete')
def test_client_delete(mock_delete):
    """ it should delete a connector by ID from API """
    mock_delete.return_value.ok = True

    client = ConnectClient(url=URL)
    client.delete('one')
    mock_delete.assert_called_once_with('{}/connectors/one'.format(URL))


@patch('kafkaconnectsync.client.requests.post')
def test_client_create(mock_create):
    """ it should create a new connector configuration """
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

    client = ConnectClient(url=URL)
    client.create(connector)
    mock_create.assert_called_once_with(
        '{}/connectors'.format(URL), json=expected_response)


@patch('kafkaconnectsync.client.requests.put')
def test_client_update(mock_put):
    """ it should update an existing connector """
    connector = {
        'config': {
            'name': 'one',
            'test': 'test',
        },
    }
    mock_put.return_value.ok = True

    client = ConnectClient(url=URL)
    client.update(connector)
    mock_put.assert_called_once_with(
        '{}/connectors/one/config'.format(URL), json=connector['config'])
