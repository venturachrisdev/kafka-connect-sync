""" Main module tests """

# Mock implementation changes between python versions. Add support for both
from kafkaconnectsync import sync
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import patch, Mock
else:
    from mock import patch, Mock

URL = 'https://my-kafka-api.app.com'

API_CONNECTORS = [
    {
        "name": "to-update-connector",
        "config": {
            "name": "to-update-connector",
            "format": "json",
            "flush.size": "2",
        }
    },
    {
        "name": "to-delete-connector",
        "config": {
            "name": "to-delete-connector",
            "format": "json",
            "flush.size": "2",
        }
    },
]

LIST_CONNECTORS = [
    {
        "config": {
            "name": "to-create-connector",
            "format": "json",
            "flush.size": "3",
        }
    },
    {
        "config": {
            "name": "to-update-connector",
            "format": "json",
            "flush.size": "3",
        }
    },
]


def test_parameters_validation():
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


@patch('kafkaconnectsync.client.requests.delete')
@patch('kafkaconnectsync.client.requests.post')
@patch('kafkaconnectsync.client.requests.get')
def test_sync_create_connectors(mock_get, mock_post, mock_delete):
    """ it should create connectors from list """
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = []
    mock_post.return_value.ok = True
    sync(url=URL, connectors=LIST_CONNECTORS, strict=False,
         wait_for_deployment=False, verbose=False)

    mock_get.assert_called_once_with('https://my-kafka-api.app.com/connectors')
    for connector in LIST_CONNECTORS:
        mock_post.assert_any_call('https://my-kafka-api.app.com/connectors', json={
            'config': connector['config'], 'name': connector['config']['name']})
    mock_delete.assert_not_called()


# @patch('kafkaconnectsync.client.requests.delete')
# @patch('kafkaconnectsync.client.requests.put')
# @patch('kafkaconnectsync.client.requests.get')
# def test_sync_update_connector(mock_get, mock_put, mock_delete):
#     """ it should update connectors from list present on the API """
#     connector = LIST_CONNECTORS[1]
#     mock_get.return_value.ok = True
#     mock_get.return_value.json.return_value = [
#         x['config']['name'] for x in API_CONNECTORS]
#     mock_put.return_value.ok = True
#     sync(url=URL, connectors=[connector], strict=False,
#          wait_for_deployment=False, verbose=False)

#     mock_get.assert_called_once_with('https://my-kafka-api.app.com/connectors')
#     mock_put.assert_called_with('https://my-kafka-api.app.com/connectors/{}'.format(connector['config']['name']), json={
#         'config': connector['config'], 'name': connector['config']['name']})
#     mock_delete.assert_not_called()


@patch('kafkaconnectsync.client.requests.delete')
@patch('kafkaconnectsync.client.requests.get')
def test_sync_delete_connector(mock_get, mock_delete):
    """ it should delete connectors present on the API that are not in the list if strict mode is enabled """
    mock_get.return_value.ok = True
    connector = API_CONNECTORS[1]
    mock_get.return_value.json.return_value = [
        x['config']['name'] for x in API_CONNECTORS]
    mock_delete.return_value.ok = True
    sync(url=URL, connectors=[LIST_CONNECTORS[0]], strict=True,
         wait_for_deployment=False, verbose=False)

    mock_get.assert_called_once_with('https://my-kafka-api.app.com/connectors')
    mock_delete.assert_called_with(
        'https://my-kafka-api.app.com/connectors/{}'.format(connector['config']['name']))
