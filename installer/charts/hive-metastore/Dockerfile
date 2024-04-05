FROM openjdk:11-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
#ARG HADOOP_VERSION=3.2.0
ARG HADOOP_VERSION=3.3.4


RUN apt-get update && \
    apt-get install -y curl procps --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=hairyhenderson/gomplate:stable /gomplate /usr/local/bin/gomplate
RUN chmod 755 /usr/local/bin/gomplate

RUN useradd --create-home appuser
USER appuser
RUN mkdir -p /home/appuser/opt

# Set Hadoop/HiveMetastore variables and Classpath
ENV USER_HOME="/home/appuser"
WORKDIR "${USER_HOME}/opt"
ENV HADOOP_HOME="${USER_HOME}/opt/hadoop"
ENV METASTORE_HOME="${USER_HOME}/opt/hive-metastore"
ENV HADOOP_CLASSPATH="${HADOOP_HOME}/share/hadoop/tools/lib/*:${METASTORE_HOME}/lib"
ENV PATH="${HADOOP_HOME}/bin:${METASTORE_HOME}/lib/:${HADOOP_HOME}/share/hadoop/tools/lib/:/opt/postgresql-jdbc.jar:${PATH}"


# Download and extract the Hadoop binary package.
RUN curl -s https://archive.apache.org/dist/hadoop/core/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz \
        | tar xz -C ${USER_HOME}/opt/  \
        && ln -s ${HADOOP_HOME}-$HADOOP_VERSION ${HADOOP_HOME} \
        && rm -r ${HADOOP_HOME}/share/doc

# Add S3a jars to the Hadoop classpath
RUN cp ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws* ${HADOOP_HOME}/share/hadoop/common/lib/ && \
    cp ${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk* ${HADOOP_HOME}/share/hadoop/common/lib/

# Download and install the standalone metastore binary 
# RUN curl -s https://repo1.maven.org/maven2/org/apache/hive/hive-standalone-metastore/3.1.3/hive-standalone-metastore-3.1.3-bin.tar.gz \
#         | tar xz -C /opt/ \
#         && ln -s /opt/apache-hive-metastore-3.1.3-bin ${METASTORE_HOME}

RUN curl -s https://apache.uvigo.es/hive/hive-standalone-metastore-3.0.0/hive-standalone-metastore-3.0.0-bin.tar.gz \
        | tar xz -C ${USER_HOME}/opt/ \
        && ln -s ${USER_HOME}/opt/apache-hive-metastore-3.0.0-bin ${METASTORE_HOME}        
# Add jars to the Hive Metastore classpath
RUN cp ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws* ${METASTORE_HOME}/lib/ && \
    cp ${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk* ${METASTORE_HOME}/lib/

# Download and install the postgres connector used by HiveMetastore
RUN curl -s https://jdbc.postgresql.org/download/postgresql-42.4.1.jar -o postgresql-42.4.1.jar && mv postgresql-42.4.1.jar ${USER_HOME}/opt/postgresql-jdbc.jar
RUN cp ${USER_HOME}/opt/postgresql-jdbc.jar  ${HADOOP_HOME}/share/hadoop/common/lib/ && chmod -R 775 ${HADOOP_HOME}/share/hadoop/common/lib/*
RUN cp ${USER_HOME}/opt/postgresql-jdbc.jar ${METASTORE_HOME}/lib/ && chmod -R 775 ${METASTORE_HOME}/lib/*



#COPY entrypoint.sh ${METASTORE_HOME}/bin/
#RUN chmod 775 ${METASTORE_HOME}/bin/entrypoint.sh

# Metastore URI Port
EXPOSE 9083

WORKDIR ${METASTORE_HOME}

# Apply Hive custom configurations and start Metastore Service through entrypoint.sh file 
#
# We need to use the exec form to avoid running our command in a subshell and omitting signals,
# thus being unable to shut down gracefully:
# https://docs.docker.com/engine/reference/builder/#entrypoint
#
# Also we need to use relative path, because the exec form does not invoke a command shell,
# thus normal shell processing does not happen:
# https://docs.docker.com/engine/reference/builder/#exec-form-entrypoint-example




CMD ["bin/entrypoint.sh"]
