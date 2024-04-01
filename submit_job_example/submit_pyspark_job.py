import json

import requests
from requests.auth import HTTPBasicAuth

url = "http://<server>/lighter/api/batches"

payload = {
  "name": "test submit job",
  "file": "local:///opt/spark/examples/src/main/python/wordcount.py",
  "args": ["/opt/spark/examples/src/main/python/logistic_regression.py"],
  "numExecutors": 1,
  "executorCores": 1,
  "executorMemory": "1G",
  "driverCores": 1,
  "driverMemory": "1G",
  "conf": {
    # "spark.kubernetes.container.image": 'ghcr.io/aisingapore/kapitan-spark/spark:0.0.1-spark3.5.0',
    "spark.kubernetes.container.image": 'secondcomet/spark',
    "spark.kubernetes.container.image.pullPolicy": 'Always',
    "spark.kubernetes.file.upload.path": 'local:///temp'
  }
}


headers = {
    'Content-Type': 'application/json'
}

username = '<user>'
password = '<password>'

response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth(username, password), data=json.dumps(payload))
