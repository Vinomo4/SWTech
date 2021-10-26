SWTech
==============================
Repository to identify different author profiles and connect how the modifications in the code affect the tech debt of a software product.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train` [!!!!!!!!! l'acabarem utilitzant? !!!!!!!!!!]
    ├── README.md          <- The top-level README for developers using this project
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   │   └── model_data.csv
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   │   └── model_data_with_clusters.csv
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details [!!!!!!! eliminar si no s'acaba utilitzant !!!!!!!!]
    │
    ├── notebooks               <- Jupyter notebooks that act as scripts for understanding and preparing data, trained and serialized models, model        │   └── Classifiers.ipynb      clusterization and model validation.
    │   └── Clustering.ipynb
    │   └── Data_preparation.ipynb
    │   └── Data_understanding.ipynb
    │   └── Validation.ipynb
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis 
    │   └── texts          <- Generated analysis in text format.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    |   └── tracking       <- Contains the activity tracked when running the scripts. The code is generated automatically.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported [SI JA TENIM EL REQUIREMENTS QUE INSTALA TOTS ELS MODULS, PERQ CAL AQUESTA?]]
    ├── src                <- Source code for use in this project.
    |   ├── automatic.py   <- Executes automatically all the code scripts stroring the obtained results.
    │   │
    │   ├── data           <- Scripts .py related to data preparation 
    │   │   └── Data_preparation.py
    │   │   └── data_cleansing.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling.
    │   │   └── basic_statistics.py
    │   │   └── data_quality.py
    │   │   └── Data_Understanding.py
    │   │   └── tracking.py
    │   │
    │   ├── models         <- Scripts to implement, train and validate clustering and classification models. 
    │   │   │                 Scripts for model validation are also included.
    │   │   ├── fun_models.py
    │   │   └── fun_validation.py
    │   │   └── fun_classifiers.py
    │   │   └── Clustering.py
    │   │   └── Validation.py
    │   │   └── Classifiers.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations [!!! eliminar tota aquesta carpeta?!!!]
    │       └── visualize.py
    │  
    ├── test_environment.py [!!! ÉS NECESSARI ?!!!]
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
    


--------

## Install Necessary Packages

__To Use Pip:__

The python and ipython packages inside the `requirements.txt` file need to be installed using the following command.

```bash
pip install -r requirements.txt
```

__To Use Sparksession:__

It is necessary to install java from https://www.java.com/en/.

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

## Deployment
The deployment process consists of giving an input author the user obtains the quality rating corresponding to the author entered as an output.
The command to use

```bash
 python3 Deployment.py --author '<name of the author>'
 ```

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
