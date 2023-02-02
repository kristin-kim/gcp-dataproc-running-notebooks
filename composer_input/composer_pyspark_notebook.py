"""Example Airflow DAG that creates a Cloud Dataproc cluster, runs the Hadoop
wordcount example, and deletes the cluster.
This DAG relies on three Airflow variables
https://airflow.apache.org/concepts.html#variables
* gcp_project - Google Cloud Project to use for the Cloud Dataproc cluster.
* gce_zone - Google Compute Engine zone where Cloud Dataproc cluster should be
  created.
* gcs_bucket - Google Cloud Storage bucket to use for result of Hadoop job.
  See https://cloud.google.com/storage/docs/creating-buckets for creating a
  bucket.
"""
import datetime
import os
from airflow import models
from airflow.contrib.operators import dataproc_operator
from airflow.utils import trigger_rule
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())
default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}

# Arguments to pass to Cloud Dataproc job.
input_notebook = "gs://notebooks-staging-bucket-kk/notebooks/jupyter/sample_notebook.ipynb"
output_notebook = "gs://notebooks-staging-bucket-kk/notebooks/jupyter/output/composer_sample_output.ipynb"
notebook_args= [input_notebook, output_notebook]

PYSPARK_JOB = {
    "reference": {"project_id": models.Variable.get('gcp_project')},
    "placement": {"cluster_name": 'composer-dnb-{{ ds_nodash }}'},
    "pyspark_job": {
        "main_python_file_uri": f"gs://notebooks-staging-bucket-kk/composer_input/jobs/wrapper_papermill.py",
        "args": notebook_args }
}
# [START composer_hadoop_schedule]
with models.DAG(
        'pyspark_notebook_execution',
        # Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    
    # Create a Cloud Dataproc cluster.
    create_dataproc_cluster = dataproc_operator.DataprocClusterCreateOperator(
        task_id='create_dataproc_cluster',
        cluster_name='composer-dnb-{{ ds_nodash }}',
        num_workers=0,
        region='us-central1',
        zone=models.Variable.get('gce_zone'),
        image_version='2.0',
        master_machine_type='n1-standard-4',
        # worker_machine_type='n1-standard-2'
        init_actions_uris=[f"gs://notebooks-staging-bucket-kk/composer_input/initialization_scripts/init_pip_gcsfuse.sh"],
        )

    # Submit a pyspark job
    pyspark_task = DataprocSubmitJobOperator(
        task_id="pyspark_task", 
        job=PYSPARK_JOB, 
        region='us-central1', 
        project_id=models.Variable.get('gcp_project'))
        
    # Delete Cloud Dataproc cluster.
    delete_dataproc_cluster = dataproc_operator.DataprocClusterDeleteOperator(
        task_id='delete_dataproc_cluster',
        region='us-central1',
        cluster_name='composer-dnb-{{ ds_nodash }}',
        # Setting trigger_rule to ALL_DONE causes the cluster to be deleted
        # even if the Dataproc job fails.
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE)

    # [START composer_hadoop_steps]
    create_dataproc_cluster >> pyspark_task >> delete_dataproc_cluster
    # [END composer_hadoop_steps]
