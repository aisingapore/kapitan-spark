
# Smoke Test
### Hive metastore and S3a

1. Run below codes in Jupyter notebook
    ```
    %%configure
    {
        "conf":{
        "spark.kubernetes.container.image.pullPolicy": "Always",
        "spark.driver.memory" : "500m",
        "spark.executor.memory": "500m",
        "spark.hadoop.fs.s3a.access.key":"user",
        "spark.hadoop.fs.s3a.secret.key": "masked",
        "spark.eventLog.dir": "s3a://some-path/spark-history-server-logs",
        "spark.eventLog.enabled": true
        }
    }
    ```
2. Test able to connect to Hive metastore
   ```
   %%sql
   show databases
   ```

### Spark Thrift Server

1. Run kubectl port forward command on Spark Thrift server pod on port 10000
    ```
    kubectl port-forward <pod-name> 10000:10000 --namespace <namespace>
    ```

2.  Open Dbeaver app and connect to localhost on port 10000. (can download from https://dbeaver.io/)

3. Given that the default configuration utilizes the load balancer on port 31002, you can directly connect to the KUBERNETES_NODE_IP using Dbeaver on port 31002, eliminating the need for port-forwarding.

### Spark History Server

1. Run below codes in Jupyter notebook
    ```
    df = spark.createDataFrame(
        [
            (1, "foo"),
            (2, "bar"),
        ],
        ["id", "label"]
    )
    df.collect()
    ```

2. Follow by pressing Kernel -> Shut down kernel on the top bar of Jupyter notebook

3. Check if the output event log is in the persistence volume or S3a

4. Open Spark History Server webpage and see the event log created
