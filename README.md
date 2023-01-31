# running-notebooks
Running notebooks on Dataproc via Cloud Composer

    .
    ├── composer_pyspark_notebook.py      # DAGs for Composer
    ├── composer_input                   # Test files (alternatively `spec` or `tests`)
    │   ├── init_pip_gscfuse.sh         # Load and stress tests
    |   │   ├── integration         # End-to-end, integration tests (alternatively `e2e`)
    |   ├── notebooks/jupyter         # End-to-end, integration tests (alternatively `e2e`)
        │   ├── integration         # End-to-end, integration tests (alternatively `e2e`)
    └── ...
    └── ...
    
    1. Create a Composer Envirionemnt
    2. Download composer_pyspark_notebook.py and upload it to DAG folder
