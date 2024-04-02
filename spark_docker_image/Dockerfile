FROM apache/spark:3.5.0


USER root
ENV DELTA_LAKE_VER 3.0.0

# Adding relevant jar files to SPARK_HOME/jars
ADD --chown=spark:spark "https://repo1.maven.org/maven2/io/delta/delta-contribs_2.12/${DELTA_LAKE_VER}/delta-contribs_2.12-${DELTA_LAKE_VER}.jar" $SPARK_HOME/jars
ADD --chown=spark:spark "https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/${DELTA_LAKE_VER}/delta-spark_2.12-${DELTA_LAKE_VER}.jar" $SPARK_HOME/jars
ADD --chown=spark:spark "https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_LAKE_VER}/delta-storage-${DELTA_LAKE_VER}.jar" $SPARK_HOME/jars

ADD --chown=spark:spark https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar $SPARK_HOME/jars
ADD --chown=spark:spark https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar $SPARK_HOME/jars
ADD --chown=spark:spark https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.490/aws-java-sdk-bundle-1.12.490.jar $SPARK_HOME/jars
# Adding GCS Connector for Spark
ADD --chown=spark:spark https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.15/gcs-connector-hadoop3-2.2.15-shaded.jar $SPARK_HOME/jars

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

USER spark
WORKDIR /opt/spark/work-dir