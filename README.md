SWTech
==============================
Repository to identify different author profiles and connect how the modifications in the code affect the tech debt of a software product.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train` [!!!!!!!!! l'acabarem utilitzant? !!!!!!!!!!]
    ├── README.md          <- The top-level README for developers using this project
    ├── data
    │   ├── external       <- Data from third party sources. [!!! està buida, eliminar? !!!]
    │   ├── interim        <- Intermediate data that has been transformed. [!!! està buida, eliminar? !!!]
    │   ├── processed      <- The final, canonical data sets for modeling. [!!! està buida, eliminar? !!!]
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details [!!!!!!! eliminar si no s'acaba utilitzant !!!!!!!!]
    │
    ├── models             <- A directory containing `.ipynb` files that contain trained and serialized models, model clusterization and model validation
    │
    ├── notebooks          <- Jupyter notebooks that act as scripts for understanding and preparing data
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials [!!!!! eliminar?!!!!!]
    │
    ├── reports            <- Generated analysis 
    │   └── figures        <- Generated graphics and figures to be used in reporting
    |   └── tracking       <- Contains the activity tracked when running the scripts. The code is generated automatically.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module [!!! eliminar? !!!]
    |   ├── automatic.py   <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data [!!! eliminar? !!!]
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── basic_statistics.py
    │   │   └── Data_preparation.py
    │   │   └── data_quality.py
    │   │   └── Data_Understanding.py
    │   │   └── preparation_data.py
    │   │   └── tracking.py
    │   │
    │   ├── models         <- Scripts to implement, train and validate clustering models. There are also all functinos used for this scripts. Validation of the models included.
    │   │   │                 predictions
    │   │   ├── F_models.py
    │   │   └── F_validation.py
    │   │   └── Models.py
    │   │   └── predict_model.py [!!! eliminar !!!]
    │   │   └── train_model.py [!!! eliminar !!!]]
    │   │   └── validation.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations [!!! eliminar tota aquesta carpeta?!!!]
    │       └── visualize.py
    │
    ├── test_environment.py [!!! ÉS NECESSARI ?!!!]
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
    


--------

## Install Necessary Packages (Acabar quan estigui fet el deployment)

__To Use Pip:__

Use `requirements.txt` to install all necessary packages for this repository (FINS QUE NO S'HAGI FET NO SÉ SI S'HAURA D'INCLOURE)

## Data
The original data tables con be obtained in two formats:
* The dataset v2.0 can be downloaded in SQLite database with [.db](https://github.com/clowee/The-Technical-Debt-Dataset/releases/tag/2.0) extension
* Alternatively, if you prefer you can download each table as a [.csv](https://drive.google.com/file/d/1QykXNMT-5DMw9j9zVE5m3UJFyUEvQiIr/view?usp=sharing)
(Note that you must have the UPC email (name.surname@estudiantat.upc.edu) in order to get access to the files..) 

These files can be used to create train, validation, testing splits: (comprovar quines taules s'utilitzen per eliminar les que no)

* `GIT_COMMIT_CHANGES.vcf`
* `GIT_COMMITS.vcf`
* `JIRA_ISSUES.xlsx` (NO?)
* `PROJECTS.csv` (NO?)
* `REFACTORING_MINER.csv`
* `SONAR_ANALYSIS`.csv`
* `SONAR_ISSUES.csv`
* `SONAR_MEASURES.csv`
* `SONAR_RULES.csv` (NO?)
* `SZZ_FAULT_INDUCING_COMMITS.csv`

To obtain more detailed information reagrding tables and high-quality diagram see https://drive.google.com/file/d/1eF23cFIq7QNx0v11BnMi_89Yh79DMVzK/view
(pensar com penjar aquest pdf ja que només tenen accés els de la UPC)

The data files used to train and evaluate the model can be find:
* Com pengem els dos datasets de la temp_data folder que conté model_data.csv i model_data_with_clusters.csv

## Workflow Overview: From original data files to trained clustering model 

The following READMEs provide details about the other scripts and options used in the entire pipeline. They detail the entire process from start (i.e., using new data in `.vcf` format) to finish (i.e., trained neural network, plots, etc.). (uff això no ho farem no? Si que podem dir l'ordre de'execucions que es fan)

1. Prepare data
2. Train model
3. Test model
4. Creation of a new quality rating associated to each cluster
5. ...

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
