FROM apache/spark:3.5.1


USER root
ENV DELTA_LAKE_VER=3.0.0

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

# zeppelin
ADD --chown=spark:spark https://repo1.maven.org/maven2/com/fasterxml/woodstox/woodstox-core/6.5.0/woodstox-core-6.5.0.jar $SPARK_HOME/jars
ADD --chown=spark:spark https://repo1.maven.org/maven2/org/codehaus/woodstox/stax2-api/4.2.1/stax2-api-4.2.1.jar $SPARK_HOME/jars
ADD --chown=spark:spark https://repo1.maven.org/maven2/org/apache/commons/commons-configuration2/2.11.0/commons-configuration2-2.11.0.jar $SPARK_HOME/jars
ADD --chown=spark:spark https://repo1.maven.org/maven2/com/google/re2j/re2j/1.8/re2j-1.8.jar $SPARK_HOME/jars

# for spark kafka streaming
ADD --chown=spark:spark https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar $SPARK_HOME/jars

# excel
ADD --chown=spark:spark https://repo1.maven.org/maven2/com/crealytics/spark-excel_2.12/3.5.1_0.20.4/spark-excel_2.12-3.5.1_0.20.4.jar $SPARK_HOME/jars
RUN chmod -R go+r $SPARK_HOME/jars


RUN apt update && apt upgrade -y && apt install -y software-properties-common unzip htop
# RUN apt-get install --reinstall ca-certificates
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt update
# RUN apt install -y python3.11
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
# RUN update-alternatives --config python3
# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

#RUN ln -sf /usr/bin/python3.11 /usr/bin/python


# RUN apt-get clean
#RUN apt-get autoremove -y --purge
#RUN rm -rf /var/lib/apt/lists/*

COPY ./installer/charts/zeppelin/env_python_3_with_R.yml /tmp/env_python_3_with_R.yml
ARG miniconda_version="py312_24.7.1-0"
# Install Miniconda with no base environment
RUN set -ex && \
    ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        MINICONDA_OS="Linux-x86_64"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        MINICONDA_OS="Linux-aarch64"; \
    else \
        echo "Unsupported architecture: $ARCH"; exit 1; \
    fi && \
    wget -nv https://repo.anaconda.com/miniconda/Miniconda3-${miniconda_version}-${MINICONDA_OS}.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    export PATH=/opt/conda/bin:$PATH && \
    conda config --set always_yes yes --set changeps1 no && \
    conda env update -f  /tmp/env_python_3_with_R.yml --prune && \
    conda clean --all -y && rm /tmp/env_python_3_with_R.yml

# Optional: Remove some unnecessary files to reduce size
RUN find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete
ENV PATH=/opt/conda/envs/python_3_with_R/bin:/opt/conda/bin:$PATH


#COPY --chown=spark:spark ./spark_docker_image/requirements.txt /tmp/requirements.txt
RUN mkdir -p /home/spark 
RUN chown -R spark:spark /home/spark

USER spark
WORKDIR /opt/spark/work-dir
# ENV PYSPARK_PYTHON=python3.11
ENV PYSPARK_PYTHON=python
# RUN pip install -r /tmp/requirements.txt --no-cache-dir && rm /tmp/requirements.txt
