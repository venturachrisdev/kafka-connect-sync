# Kakfa Connect Sync
Kafka Connect API connectors synchronization library

## About

## Installing

Install using pip:
```sh
$ pip3 install kafkaconnectsync
```
Or you can simply add `kafkaconnectsync` package to your `requirements.txt` file.

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

# ...
# Deploy your app...
# ...

sync(url, connectors, wait_for_deployment=True, verbose=True)
```

## Documentation

* `sync(url, connectors, wait_for_deployment=True, verbose=False)`:
    - **url**: You Kafka Connect API hostname.
    - **connectors**: The array of connectors objects to sync on Kafka Connect. Default: `[]`.
    - **wait_for_deployment**: Set this flag to `True` if your integrating this script to your app deployment and you want `sync` to wait until your API is available. Default: `True`.
    - **verbose**: Set this flag to `True` if you want to output sync actions to your terminal. Default: `false`.

## Contributors
- Christopher Ventura <<chrisventura.work@gmail.com>>
