# running-notebooks
Running notebooks on Dataproc via Cloud Composer

    .
    ├── composer_pyspark_notebook.py      # DAGs for Composer
    ├── composer_input                   # Test files (alternatively `spec` or `tests`)
    │   ├── init_pip_gscfuse.sh         # Load and stress tests
wrapper.py
Runs a papermill execution of input notebook and writes the output file into the assgined location

Notebook
sample_notebook.ibynp # verify if GCS buckets are mounted at pwd as a file system
verify .py files in mounted GCS buckets are executable via !python and %run command
    
    1. Create a Composer Envirionemnt
    2. Download composer_pyspark_notebook.py and upload it to DAG folder
