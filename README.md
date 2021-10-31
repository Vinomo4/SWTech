SWTech
==============================
Repository to identify different author profiles and connect how the modifications in the code affect the tech debt of a software product.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   │   └── model_data.csv
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   │   └── model_data_with_clusters.csv
    │   └── raw            <- The original, immutable data dump.
    │
    │
    ├── notebooks               <- Jupyter notebooks that act as scripts for understanding and preparing data, trained and serialized models, model        │   └── Classifiers.ipynb      clusterization and model validation.
    │   └── Classifiers.ipynb
    │   └── Clustering.ipynb
    │   └── Data_Preparation.ipynb
    │   └── Data_Understanding.ipynb
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
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported.
    ├── src                <- Source code for use in this project.
    |   ├── automatic.py   <- Executes automatically all the code scripts stroring the obtained results.
    │   │
    │   ├── data           <- Scripts .py related to data preparation 
    │   │   └── Data_preparation.py
    │   │   └── data_cleansing.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling (also includes tracking and querying scripts).
    │   │   └── basic_statistics.py
    │   │   └── Check_tracking.py
    │   │   └── data_quality.py
    │   │   └── Data_Understanding.py
    │   │   └── Query.py
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
    │   └── automatic.py  <- Automatically executes all the project scripts.
    │  
    └── test_environment.py 

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

To obtain more detailed information regarding tables and high-quality diagrams see https://drive.google.com/file/d/1eF23cFIq7QNx0v11BnMi_89Yh79DMVzK/view
(pensar com penjar aquest pdf ja que només tenen accés els de la UPC)

The data files used to train and evaluate the model can be found:
* Com pengem els dos datasets de la temp_data folder que conté model_data.csv i model_data_with_clusters.csv

## Workflow Overview: From original data files to trained clustering model 

The following points describes the entire pipeline from start (using raw data) to finish (i.e., trained clustering model, plots, etc.).

1. Data understanding: Data quality & Data Exploration
2. Data Preparation
3. Data Reduction
4. Train model
5. Creation of a new quality rating assigned to each cluster
6. Evaluation

## Deployment
The deployment process consists of giving an input author the user obtains the quality rating corresponding to the author entered as an output.
The command to use

```bash
 python3 Deployment.py --author '<name of the author>'
 ```

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
