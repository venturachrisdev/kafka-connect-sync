# Kafka Connect Sync

Kafka Connect API connectors synchronization library

## About

The `kafkaconnectsync` library allows you to incorporate the Kafka Connect connectors/sink to your deployment code.

When running Kafka Connect in distribute mode, connectors need to be added using REST methods after the API is running. Creating connectors shouldn't be a manual process so kafkaconnectsync provides functions to manage connectors as an infrastructure/deployment component.

To sync connectors, kafkaconnectsync reads the list of connectors and decides if it needs to create, update or delete them depending on the status of the API (i.e the existing connectors).

## Installing

Install using pip:
```sh
$ pip3 install kafkaconnectsync
```

Alternatively, you can use `setup.py` to install by cloning this repository and running:
```sh
$ python setup.py install
```

## Usage
1. Define your connectors:

```json
# connectors.json

[
    {
        "config": {
            "name": "my_connector_name",
            "properties": "values"
        }
    },
    {
        "config": {
            "name": "my_connector_name_two",
            "properties": "values"
        }
    }
]
```

2. Import the `sync` function from the package. Make sure to call it after your app deployment has been done.
```python
# Other imports...
import sync from kafkaconnectsync

url = 'https://my-kafka-connect-api.com'
connectors = json.loads(open('connectors.json'))

"""
 ...
 Deploy your app here...
 ...
"""

# Sync connectors
sync(url, connectors, strict=True, wait_for_deployment=True, verbose=True)
```

## Documentation

* `sync(url, connectors=[], wait_for_deployment=True, verbose=False)`:
    - **url**: You Kafka Connect API hostname.
    - **connectors**: The array of connectors objects to sync on Kafka Connect. Default: `[]`.
    - **strict**: When `strict` is enabled, apart from creating/updating connectors from the list, the sync function will remove all the API connectors that are not present on this list as a way to synchronize your list with the API. Default: `True`
    - **wait_for_deployment**: If `True`, it will keep sending requests to the Kafka Connect hosts until it becomes available. Useful if your deploying your app and the function should wait for the deployment to finish. Default: `True`.
    - **verbose**: Set this flag to `True` if you want to output action logs to your terminal. Default: `False`.

## Contributors

- Christopher Ventura <<chrisventura.work@gmail.com>>
