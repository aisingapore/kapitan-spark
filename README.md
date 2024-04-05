# Kapitan Spark - All-in-One Spark Installer for Kubernetes!

<img src="img/logo.png">


# Overview 
Welcome to our Helm Chart Installer for Spark. This would enable a user to easily deploy the Spark Ecosystem Components on a Kubernetes Cluster.


The below components enable the following features:
1. Running Spark Notebooks using Spark and Spark SQL
2. Creating Spark Jobs using python
3. Tracking Spark Jobs using a UI


Components:
- Hive Metastore
- Spark Thrift Server
- Spark History Server
- Lighter Server
- Jupyter Lab with SparkMagic Kernel



We invite you to try this out and let us know any issues/feedback you have via Github Issues. Do let us know what adaptions you have done for your setup via Github Discussions.



## Customisation of the Helm Chart

This helm chart supports various methods of customization
1. Modifying `values.yaml`
2. Providing a new `values.yaml` file
3. Using Kustomize

<details><summary>Show Details of Customization</summary>

### Customising values.yaml
You may customise your installation of the above components by editing the file at [installer/values.yaml](installer/values.yaml).

### Alternative Values File
Alternatively, you can create a copy of the values file and run the following modified command
```bash
 helm install spark-bundle installer --values new_values.yaml --namespace kapitanspark --create-namespace
 ```

### Using Kustomize :
This approach prevents you from modifying the original source code and enables you to customize as per your needs.

You may refer to this section [Advanced Installation](#advanced-installation)
</details>


### Installing Components Separately

If you want to install each component separately, you can also navigate to the individual chart folder and run `helm install` as needed.

### Creating Multiple Instances 

You may create multiple instances of this Helm Chart by specifying a different Helm Chart name, for example : production, staging and testing environments.

<details><summary><b>Show sample commands</b></summary>

```bash 
helm install spark-production installer --namespace kapitanspark-prod --create-namespace
```

```bash 
helm install spark-testing installer --namespace kapitanspark-test --create-namespace
```

</details>








## Usage

### Quick Start
Suitable for users with basic knowledge on Kubernetes and Helm. Can also install on Microk8s.

Requirements:
- Ingress
- Storage that support `ReadWriteMany`

<details><summary><b>Show instructions</b></summary>



#### (Optional) Setup of Local Kubernetes Cluster
You may skip the local setup if you already an existing kubernetes cluster you would like to use


<details><summary>See details of setup for `microk8s` </summary>
At the moment, we have only tested this locally using `microk8s` and `minikube` 

1. If you are using Microk8s, below are the steps to install Nginx and PV with RWX support:

    ```sh
    microk8s enable hostpath-storage
    microk8s enable ingress
    ```

</details>

#### Installation of Helm Chart
2. Choose which components you need by enabling/disabling them at `installer/values.yaml`.

3. Run the following install command, where `spark-bundle` is the name you prefer:

    ```sh
    helm install spark-bundle installer --namespace kapitanspark --create-namespace
    ```
4. If any errors occur during the installation step, run the command below to uninstall it. The `--wait` flag will ensure all pods are removed.
   ```sh
   helm uninstall spark-bundle --namespace kapitanspark --wait
   ```
5. Run the command `kubectl get ingress --namespace kapitanspark` to get IP address of KUBERNETES_NODE_IP. For default password, please refer to component section in this document. After that you can access 
    - Jupyter lab at http://KUBERNETES_NODE_IP/jupyterlab 
    - Spark History Server at http://KUBERNETES_NODE_IP/spark-history-server
    - Lighter UI http://KUBERNETES_NODE_IP/lighter 

</details>


### Advanced Installation and Customisation
This method is ideal for advanced users who have some expertise in Kubernetes and Helm. 
This approach enables you to extend existing configurations efficiently for your needs, without modifying the existing source code.

<details><summary><b>Show instructions</b></summary>

Requirements:
- Ingress (Nginx)
- Storage that support `ReadWriteMany` , eg: NFS or Longhorn NFS

1. Customize your components by enabling or disabling them in `installer/values.yaml`

2. Navigate to the directory `kcustomize/example/prod/`, and modify `google-secret.yaml` and `values.yaml` files.

3. Modify `jupyterlab/requirements.txt` according to your project before installation

4. Execute the install command stated below in the folder `kcustomize/example/prod/`, replacing `spark-bundle` with your preferred name. You can add `--dry-run=server` to test any error in helm files before installation:
    ```sh
    cd kcustomize/example/prod/
    helm install spark-bundle ../../../installer --namespace kapitanspark  --post-renderer ./kustomize.sh --values ./values.yaml --create-namespace
    ```
5. If any errors occur during the installation step, run the command below to uninstall it. The `--wait` flag will ensure all pods are removed.
   ```sh
   helm uninstall spark-bundle --namespace kapitanspark --wait
   ```

6. After successful installation, you should be able to access the Jupyter Lab, Spark History Server and Lighter UI based on your configuration of the Ingress section in `values.yaml`.


</details>

### Compatibility 
| Syntax      | Description |
| ----------- | ----------- |
| Kubernetes      | 1.23.0 >= 1.29.0       |
| Helm   | 3        |


### Component Details and Defaults
<details><summary><b>Remarks</b></summary>

- Hive metastore
    - You may rebuild the image using the Dockerfile `hive-metastore/Dockerfile`
    - After rebuilding, modify the following keys in `values.yaml`:  `image.repository`, `image.tag` in `values.yaml`.
- Spark Thrift Server
    - You may rebuild the image using the Dockerfile `spark_docker_image/Dockerfile`
    - After rebuilding, modify the following keys in `values.yaml`: `image.repository`, `image.tag` in `values.yaml`.
    - Spark UI has been intentionally disabled at `spark-thrift-server/templates/service.yaml`.
    - Dependency: `hive-metastore` component.

- Jupyter Lab
    - Modify `jupyterlab/requirements.txt` according to your project before installation.
    - Default password: `spark ecosystem`

- Lighter 
    - You may rebuild the image using the Dockerfile `spark_docker_image/Dockerfile` 
    - After rebuilding, modify the following keys in `values.yaml`: `image.spark.repository`, `image.spark.tag` in `values.yaml`.
    - If Spark History Server uses Persistent Volumes to save event logs instead of Blob storage S3a, ensure to install it with `spark-history-server` component on the same Kubernetes namespace.
    - Dependencies: `hive-metastore` and `spark-history-server` components. The latter can be turned off in `values.yaml`.
    - Default user: `dataOps` password: `5Wmi95w4`

- Spark History Server
    - By default, Persistent Volumes is used to read event logs, you may modify this by updating the `dir` key in [`spark-history-server/values.yaml`](installer/charts/spark-history-server/values.yaml) and in the `lighter` component, update key `spark.history.eventLog.dir` in [`lighter/values.yaml`](installer/charts/lighter/values.yaml)
    - If using Persistence volume instead of Blob storage S3a, ensure it is installed on the same namespace as other components.
    - Default user: `dataOps` password: `5Wmi95w4`
</details>



----
