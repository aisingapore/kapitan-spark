FROM apache/zeppelin:0.12.0
# apache/zeppelin only support x86, no arm64
USER root

COPY ./installer/charts/zeppelin/env_python_3_with_R.yml /tmp/env_python_3_with_R.yml

RUN rm -rf /opt/conda
ARG miniconda_version="py312_24.7.1-0"
ARG miniconda_sha256="33442cd3813df33dcbb4a932b938ee95398be98344dff4c30f7e757cd2110e4f"
# Install Miniconda with no base environment
RUN set -ex && \
    wget -nv https://repo.anaconda.com/miniconda/Miniconda3-${miniconda_version}-Linux-x86_64.sh -O miniconda.sh && \
    echo "${miniconda_sha256} miniconda.sh" > anaconda.sha256 && \
    sha256sum --strict -c anaconda.sha256 && \
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


COPY --chown=185:185 --from=ghcr.io/aisingapore/kapitan-spark/spark:0.0.7-spark3.5.1 /opt/spark/ /opt/spark/

# below is custom to follow spark docker image
RUN groupadd -r spark -g 185 && \
    useradd -r -u 185 -g spark spark

RUN chown -R spark:spark "${ZEPPELIN_HOME}"
USER 185
WORKDIR /opt/spark/work-dir
ENV SPARK_HOME=/opt/spark/