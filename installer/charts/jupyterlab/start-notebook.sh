#!/bin/bash
# Shim to emit warning and call start-notebook.py
echo "WARNING: Use start-notebook.py instead"

conda install sparkmagic -y
pip install -r /tmp/requirements.txt  --no-cache-dir
jupyter nbextension enable --py --sys-prefix widgetsnbextension
jupyter-kernelspec install --user $(pip show sparkmagic | grep Location | cut -d" " -f2)/sparkmagic/kernels/pysparkkernel
jupyter serverextension enable --py sparkmagic
jupyter kernelspec uninstall sparkkernel -y
jupyter kernelspec uninstall sparkrkernel -y
jupyter kernelspec uninstall python3 -y
mkdir -p /home/jovyan/.sparkmagic/
cp /tmp/sparkmagic.json /home/jovyan/.sparkmagic/config.json
cp /tmp/*.ipynb /home/jovyan/work/

exec /usr/local/bin/start-notebook.py "$@"