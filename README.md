# running-notebooks
Running notebooks on Dataproc via Cloud Composer

    .
    ├── composer_pyspark_notebook.py      # DAGs for Composer
    ├── composer_input                   
    │   ├── init_pip_gscfuse.sh          
* **wrapper.py**: runs a papermill execution of input notebook and writes the output file into the assgined location
* **init_pip_gscfuse.sh**: this script completes following two tasks
  * Installs desired python packages 
  * Installs [gcsfuse](https://github.com/GoogleCloudPlatform/gcsfuse/blob/master/docs/installing.md) and mounts the desired bucket to the path
* **composer_pyspark_notebook.py**: 
  * Dataproc Cluster Creation 
    ```
      create_dataproc_cluster = dataproc_operator.DataprocClusterCreateOperator()
    ```
  * Dataproc PySpark Job submission
    ```
      pyspark_task = DataprocSubmitJobOperator()
    ```
  * Dataproc Cluster Deletion
    ```
      delete_dataproc_cluster = dataproc_operator.DataprocClusterDeleteOperator()
    ```
* *sample_notebook.ibynp*:
  * verify if GCS buckets are mounted at pwd as a file system
  * verify Python files in mounted GCS buckets are executable via *!python* and *%run* command
    ```
    !ls /path-1 
    !sudo python /path-1/sample.py
    %run /path-1/sample.py
    ```
## Objective
This document is intended to walk through how to migrate and run a Notebook on a Dataproc cluster using Cloud Composer. This document should not be used as a design document. 

## Orchestrating End to End Notebook Execution workflow in Cloud Composer 
a. Create a Cloud Composer Environment

b. Add DAGs file (ex. composer_pyspark_notebook.py) to the DAGs folder (found in Environment Configuration) to trigger DAGs:

    DAG folder from Cloud Composer Console ![Screenshot 2023-02-07 at 9 04 12 AM](https://user-images.githubusercontent.com/123537947/217266654-f7a017fb-7470-4e04-9803-a72be6f652bd.png)

c. Have all the files available in GCS bucket, except DAGs file which should go into your Composer DAGs folder
    
![image](https://user-images.githubusercontent.com/123537947/215648916-811a8331-b61a-45a5-8f5a-b61f3fd4fdd0.png)

## Best practices and recommendations
* Execute Notebooks on Ephemeral clusters
Orchestrate the Notebooks on ephemeral clusters. Refer to the Dataproc best practices documentation when setting up ephemeral clusters.

* Orchestration
Orchestrate the cluster creation, job execution and deletion using Dataproc Workflow templates and Cloud Composer. 

* Setup Persistent History Server
Setup Persistent History Server (PHS) to store the event logs. Here are the best practices of setting up PHS. 
https://cloud.google.com/blog/products/data-analytics/running-persistent-history-servers

* Use Custom Images
If you have dependencies that must be shipped with the cluster, such as Python libraries to be installed on all nodes, or specific security hardening software or virus protection software requirements for the image, you should consider creating a custom image for cluster creation. This will reduce the start time immensely. 

* Control the location of your initialization actions
For production usage, before creating clusters, it is strongly recommended that you place initialization actions in a centralized Cloud Storage bucket or a folder to guarantee consistent use of the same initialization action code across all Dataproc cluster nodes. It will prevent unintended upgrades from upstream in the cluster.

* Dataproc Release Notes
To stay on top of all the latest changes, review these weekly release notes which accompany each change to Cloud Dataproc. 

* Mount Cloud Storage buckets via Initialization Script
Leverage gcs-fuse to mount Cloud Storage buckets as file systems, configure gcs-fuse via initialization script. 


