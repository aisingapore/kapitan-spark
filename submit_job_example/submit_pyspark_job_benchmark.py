import json

import requests
from requests.auth import HTTPBasicAuth

url = "http://lighter.dataops-workshop.aisingapore.net/lighter/api/batches"

payload = {
  "name": "benchmark",
  "file": "s3a://dsp-aiap18-aut0/cw_benchmark/benchmark_job.py",
  "conf": {
    "spark.kubernetes.container.image.pullPolicy": 'Always',    
    "spark.kubernetes.executor.podNamePrefix": "tpcds-worker",
    "spark.sql.warehouse.dir": "s3a://dsp-aiap18-aut0/database",
    "spark.driver.memory" : "8G",
    "spark.executor.memory": "4G",
    "spark.kubernetes.driver.secretKeyRef.AWS_ACCESS_KEY_ID": "ecs-secret-2g88gf:AWS_ACCESS_KEY_ID",
    "spark.kubernetes.executor.secretKeyRef.AWS_ACCESS_KEY_ID": "ecs-secret-2g88gf:AWS_ACCESS_KEY_ID",
    "spark.kubernetes.driver.secretKeyRef.AWS_SECRET_ACCESS_KEY": "ecs-secret-2g88gf:AWS_SECRET_ACCESS_KEY",
    "spark.kubernetes.executor.secretKeyRef.AWS_SECRET_ACCESS_KEY": "ecs-secret-2g88gf:AWS_SECRET_ACCESS_KEY",
    "spark.plugins": "ch.cern.HDFSMetrics,ch.cern.CloudFSMetrics",
    "spark.cernSparkPlugin.cloudFsName": "s3a,gs",
    "spark.executor.metrics.fileSystemSchemes": "file"
  }
}


headers = {
    'Content-Type': 'application/json'
}

username = 'dataOps'
password = 'F6i1857ekrNs'

response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth(username, password), data=json.dumps(payload))
