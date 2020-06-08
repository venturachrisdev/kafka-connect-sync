from kafkaconnectsync import sync
import json

url = 'https://kafka-connect-api.my-app.io'
connectors = json.loads(open('connectors.json').read())

"""
 ...
 Deploy your app here...
 ...
"""

# Sync connectors
sync(url, connectors, strict=True, wait_for_deployment=True, verbose=True)
