FROM apache/spark:3.5.1


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
# S3 Committer for Spark 3.5.1
ADD --chown=spark:spark https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.12/3.5.1/spark-hadoop-cloud_2.12-3.5.1.jar $SPARK_HOME/jars

# spark dashboard
ADD --chown=spark:spark https://repo1.maven.org/maven2/ch/cern/sparkmeasure/spark-plugins_2.12/0.3/spark-plugins_2.12-0.3.jar $SPARK_HOME/jars
ADD --chown=spark:spark https://repo1.maven.org/maven2/ch/cern/sparkmeasure/spark-measure_2.12/0.24/spark-measure_2.12-0.24.jar $SPARK_HOME/jars


RUN apt update && apt upgrade -y && apt install -y software-properties-common unzip htop
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --config python3
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN apt-get clean
RUN apt-get autoremove -y --purge
RUN rm -rf /var/lib/apt/lists/*

COPY --chown=spark:spark ./spark_docker_image/requirements.txt /tmp/requirements.txt
RUN mkdir -p /home/spark 
RUN chown -R spark:spark /home/spark

USER spark
WORKDIR /opt/spark/work-dir
ENV PYSPARK_PYTHON=python3.11
RUN pip install -r /tmp/requirements.txt --no-cache-dir && rm /tmp/requirements.txt
