# Kapitan Spark - All-in-One Spark Installer for Kubernetes!

<img src="img/logo.png">

We're delighted to welcome you to this ultimate GitHub repository, a host for Helm multi-chart installer for Spark. Here, deploying essential Spark components on Kubernetes is made as simple as possible. With just Nginx and a ReadWriteMany (RWX) Persistent Volume ready, you're merely one Helm install command away from having your Spark components up and running!

This repository includes indispensable components like Hive Metastore, Spark Thrift Server, Lighter, Jupyter Lab, and the Spark History Server. You have the freedom to select required components for installation from the config file installer/values.yaml.

To meet the diverse needs of different organisations, our Helm installer supports the creation of multiple instances. This feature accommodates environments which require distinct setups for scenarios such as production, staging, and testing. You simply need to provide a different name to the Helm installer.

For installing standalone components, navigate to the desired individual charts/ folder and execute the Helm install command. This allows you to add individual components as per your necessity.

The customization of Helm values.yaml can be done by passing ---values new_values.yaml file during installation. Similarly, if you want to modify any *.yaml file in the template/ folder, you can do this by passing --post-renderer ./kustomize.sh. Refer to the example command in the sections below for practical guidance. This approach prevents you from modifying the original source code and enables you to customize as per your organisation's needs.

We encourage you to explore, adapt and utilize this repository to its fullest potential. It's time you experienced a remarkably effortless Spark component installation.


## Usage

### Basic Installation
Suitable for starters with little knowledge on Kubernetes and Helm. Can also install on Microk8s.

<details><summary><b>Show instructions</b></summary>

1. If you are using Microk8s, below are the steps to install Nginx and PV with RWX support:

    ```sh
    microk8s enable hostpath-storage
    microk8s enable ingress
    ```

2. Choose which components you need by enabling/disabling them at `installer/values.yaml`.

3. Run the following install command, where `spark-bundle` is the name you prefer:

    ```sh
    helm install spark-bundle installer --namespace kapitanspark --create-namespace
    ```
4. Run the command `kubectl get ingress --namespace kapitanspark` to get IP address of KUBERNETES_NODE_IP. For default password, please refer to component section in this document. After that you can access 
    - Jupyter lab at http://KUBERNETES_NODE_IP/jupyterlab 
    - Spark History Server at http://KUBERNETES_NODE_IP/spark-history-server
    - Lighter UI http://KUBERNETES_NODE_IP/lighter 

</details>


### Advanced Installation
This method is ideal for individuals who possess some expertise in Kubernetes and Helm. This approach enables you to extend existing configurations efficiently, be it setting up HTTPS, changing secret credentials, or passing Google service account credentials. Most importantly, you can achieve all these without having to make any modifications to the existing source code— a significant advantage that empowers you to maintain system integrity whilst customising to your needs.

<details><summary><b>Show instructions</b></summary>

1. Pre-installation step for existing Kubernetes with Nginx and Persistence Volume having RWX storage class supported (Example NFS or Longhorn).

2. Customize your components by enabling or disabling them in installer/values.yaml.

3. Navigate to the directory `kcustomize/example/prod/`, and modify `google-secret.yaml` and `values.yaml` files.

4. Modify `jupyterlab/requirements.txt` according to your project before installation

5. Execute the install command stated below in the folder kcustomize/example/prod/, replacing `spark-bundle` with your preferred name. You can add `--dry-run=server` to test any error in helm files before installation:
    ```sh
    cd kcustomize/example/prod/
    helm install spark-bundle ../../../installer --namespace kapitanspark  --post-renderer ./kustomize.sh --values ./values.yaml --create-namespace
    ```

6. After successful installation, you should be able to access the Jupyter Lab, Spark History Server and Lighter UI based on your configuration of the Ingress section in `values.yaml`.


</details>

### Compatibility 
| Syntax      | Description |
| ----------- | ----------- |
| Kubernetes      | 1.23.0 >= 1.29.0       |
| Helm   | 3        |


### Component 
<details><summary><b>Remarks</b></summary>

- Hive metastore
    - `hive-metastore/Dockerfile` is available for rebuilding. Post rebuilding, modify `image.repository`, `image.tag` in `values.yaml`.
- Spark Thrift Server
    - Use `spark_docker_image/Dockerfile` for a rebuild. Later, adjust `image.repository`, `image.tag` in `values.yaml`.
    - Spark UI has been intentionally disabled at `spark-thrift-server/templates/service.yaml`.
    - Dependency: `hive-metastore` component.

- Jupyter Lab
    - Modify `jupyterlab/requirements.txt` according to your project before installation.
    - Default password: `spark ecosystem`

- Lighter 
    - Utilize `spark_docker_image/Dockerfile` for rebuilding. After rebuilding, modify `image.spark.repository`, `image.spark.tag` in `values.yaml`.
    - If Spark history uses Persistence Volume to save event log instead of Blob storage S3a, ensure to install it with `spark-history-server` component on the same Kubernetes namespace.
    - Dependencies: `hive-metastore` and `spark-history-server` components. The latter can be turned off in `values.yaml`.
    - Default user: `dataOps` password: `5Wmi95w4`

- Spark History Server
    - By default, Persitence volume is used to read event log, to change update the `dir` key in `values.yaml` and in the `lighter` component, update `spark.history.eventLog.dir` key.
    - If using Persistence volume instead of Blob storage S3a, ensure it is installed on the same namespace as other components.
    - Default user: `dataOps` password: `5Wmi95w4`
</details>



----
