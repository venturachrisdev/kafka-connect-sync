from kafkaconnectsync import sync
import json

url = 'https://kafka-connect-api.my-app.io'
connectors = json.loads(open('connectors.json'))

# ...
# Deploy your app
# ...

sync(url, connectors, wait_for_deployment=True, verbose=True)
