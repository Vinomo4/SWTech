# Introduction
# Data preparation of the TechDebt dataset. Concretely, from the following tables:
# - GIT_COMMITS
# - GIT_COMMITS_CHANGES
# - JIRA_ISSUES
# - SONAR_ANALYSIS
# - SONAR_ISSUES
# - SONAR_MEASURES
 
# Import libraries and packages
# Miscellaneous libraries
import numpy as np
import pandas as pd
import os
from datetime import datetime
import collections


from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
os.getcwd()
os.chdir( '../src/features')
from tracking import track
from preparation_data import delete_na, analyse_categorical_variables, one_hot_encoding, message_length,change_commits_to_authors

track("-"*25 + "DATA PREPARATION" + "-"*25)

 
# Data Preparation
track("Defining path of the data files")
# Define the path of the data files
path1 = '../../data/raw/'
path2 = "../data/raw/"
path_git_commits = path1 + 'GIT_COMMITS.csv'
path_git_commits_changes = path2 + 'GIT_COMMITS_CHANGES.csv'
path_jira_issues = path1 + 'JIRA_ISSUES.csv'
path_sonar_analysis = path1 + 'SONAR_ANALYSIS.csv'
path_sonar_issues = path1 + 'SONAR_ISSUES.csv'
path_sonar_measures = path1 + 'SONAR_MEASURES.csv'

# Ensure the input file exist
assert os.path.isfile(path_git_commits), f'{path_git_commits} not found. Is it a file?'
assert os.path.isfile("../"+path_git_commits_changes), f'{path_git_commits_changes} not found. Is it a file?'
assert os.path.isfile(path_jira_issues), f'{path_jira_issues} not found. Is it a file?'
assert os.path.isfile(path_sonar_analysis), f'{path_sonar_analysis} not found. Is it a file?'
assert os.path.isfile(path_sonar_issues), f'{path_sonar_issues} not found. Is it a file?'
assert os.path.isfile(path_sonar_measures), f'{path_sonar_measures} not found. Is it a file?'
track("Finishing defining path of the data files")

track("Reading files")
# Read the files
git_commits_changes = spark.read.csv(path_git_commits_changes,header=True).toPandas()
git_commits = pd.read_csv(path_git_commits)
jira_issues = pd.read_csv(path_jira_issues)
sonar_analysis = pd.read_csv(path_sonar_analysis)
sonar_issues = pd.read_csv(path_sonar_issues)
sonar_measures = pd.read_csv(path_sonar_measures)
track("Finishing reading files")

# In the following section we are only selecting the useful variables for the project. The election process has been studied previusly, in the Data Understanding step.
# Define variables of interest for each dataframe
git_commits_changes_names = ['COMMIT_HASH','LINES_ADDED','LINES_REMOVED']
git_commits_names = ['PROJECT_ID','COMMIT_HASH','AUTHOR','AUTHOR_TIMEZONE','COMMIT_MESSAGE']
jira_issues_names = ['HASH']
sonar_analysis_names = ['PROJECT_ID','ANALYSIS_KEY','REVISION']
sonar_issues_names = ['CREATION_ANALYSIS_KEY','SEVERITY','STATUS','EFFORT','MESSAGE','START_LINE','END_LINE','CLOSE_ANALYSIS_KEY']
sonar_measures_names = ['analysis_key','complexity' ,'cognitive_complexity', 'coverage', 'duplicated_blocks', 'duplicated_files', 
                        'duplicated_lines_density', 'violations','blocker_violations','critical_violations','major_violations','minor_violations','info_violations','false_positive_issues','open_issues','reopened_issues','confirmed_issues', 'sqale_debt_ratio','code_smells','bugs','reliability_rating','vulnerabilities','security_rating','files', 'comment_lines_density']
# Select variables of interest
git_commits_changes = git_commits_changes[git_commits_changes_names]
git_commits = git_commits[git_commits_names]
jira_issues = jira_issues[jira_issues_names]
sonar_analysis = sonar_analysis[sonar_analysis_names]
sonar_issues = sonar_issues[sonar_issues_names]
sonar_measures = sonar_measures[sonar_measures_names]
track("Finishing selecting variables of interest for each dataframe")

track("Starting defining numercial types")
# Select columns of interest
dtypes = ['uint8','int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'object']
dtypes_num = dtypes[:-1]
track("Finishing defining numercial types")

# Deleting all NA values from the tables by using the global function implemented above delete_na().
track("Starting analysing NA values from all tables")
tables = [sonar_measures, sonar_issues, sonar_analysis, jira_issues,git_commits, git_commits_changes]
[sonar_measures, sonar_issues, sonar_analysis, jira_issues,git_commits, git_commits_changes] = delete_na(tables, dtypes)
sonar_measures = sonar_measures.reset_index(drop = True)
sonar_issues = sonar_issues.reset_index(drop = True)
sonar_analysis = sonar_analysis.reset_index(drop = True)
jira_issues = jira_issues.reset_index(drop = True)
git_commits = git_commits.reset_index(drop = True)
git_commits_changes = git_commits_changes.reset_index(drop = True)
# Moreover, in the GIT_COMMITS table, we also find rows that contain the value "No Author" in the AUTHOR column.
# As we cannot know if all those commits come from an unique unidentified person or from multiple ones, we decided to eliminate such rows, as seen in the Data Quality task, they represent a minor percentage of the table length.
# Delete rows that contain missing authors and reseting the DF index.",
git_commits = git_commits.drop(git_commits[git_commits.AUTHOR == "No Author"].index)
git_commits = git_commits.reset_index(drop= True)
track("Finishing analysing NA values from all tables")

# Categorical Values
# The next step is to analyse the categorical variables and encoding them.
# For the SONAR_MEASURES, JIRA_ISSUES, SONAR_ANALYSIS table (add more if necessary) there are not categorical varibles.
track("Starting analysing categorical variables")
table_names = ["SONAR_ISSUES"]
variable_names = [["SEVERITY", "STATUS"]]
dataframes = [sonar_issues]
analyse_categorical_variables(table_names, variable_names, dataframes)

# As can be seen in the chunk above, the SEVERITY and STATUS variables have 5 and 1 levels respectively. In our case, we have performed the One-hot encoding for the SEVERITY variable. For the STATUS variable, efore deleting all NA, there was the OPENED level. However, all rows with an OPENED status contained NA, which means that for this variable we only have the CLOSED level. 
# When joining the tables, we will calulate the mean of each types each author has.
sonar_issues = one_hot_encoding(sonar_issues, "SEVERITY")
sonar_issues = one_hot_encoding(sonar_issues, "STATUS")
track("Finishing analysing categorical variables from all tables")
 
# MESSAGE and COMMIT_MESSAGE variables
# In the following section, we will encode the MESSAGE and COMMIT_MESSAGE variables for the SONAR_ISSUES table and GIT_COMMITS table respectively. For those variables, we will calulate the length of the message for each issue/commit, and reassigning the column with that new value instead of the text from the original message.
track("Starting codifying MESSAGE and COMMIT_MESSAGE variables using message_length() function")
message_length(sonar_issues,"MESSAGE")
message_length(git_commits,"COMMIT_MESSAGE")
track("Finishing codifying MESSAGE and COMMIT_MESSAGE variables using message_length() function")
 
# ISSUE_CODE_LENGTH variable
# In the following cells we will proceed to computate the length mean per issue with the START_LINE and END_LINE variables.
track("Starting creating ISSUE_CODE_LENGTH variable for SONAR_ISSUES table")
issue_length = []
for index, row in sonar_issues.iterrows():
    diff = row['END_LINE'] - row['START_LINE']
    issue_length.append(diff)
sonar_issues = sonar_issues.drop('START_LINE', axis=1)
sonar_issues = sonar_issues.drop('END_LINE', axis=1)
sonar_issues['ISSUE_CODE_LENGTH'] = issue_length

# Joins
# To execute the Join operation, first we will focus on the Sonar tables.
# In order to execute the groupby functions, first we need to associate each commit to
# an author in the sonar_complete table. To do so, a dictionary of commit- author will be created.
commit_author_dict = {}
for i in range(len(git_commits)):
    commit_author_dict[git_commits["COMMIT_HASH"][i]] = git_commits["AUTHOR"][i]

track("Starting joining SONAR tables")
# Joining SONAR_ANALYSIS with SONAR_ISSUES
sonar_issues_complete_1 = pd.merge(sonar_issues, sonar_analysis, left_on='CREATION_ANALYSIS_KEY', right_on='ANALYSIS_KEY', how='inner')
sonar_issues_complete_2 = pd.merge(sonar_issues, sonar_analysis, left_on='CLOSE_ANALYSIS_KEY', right_on='ANALYSIS_KEY', how='inner')
sonar_issues_complete_1 = sonar_issues_complete_1.drop(['CREATION_ANALYSIS_KEY','CLOSE_ANALYSIS_KEY','ANALYSIS_KEY'], axis=1)
sonar_issues_complete_2 = sonar_issues_complete_2.drop(['CREATION_ANALYSIS_KEY','CLOSE_ANALYSIS_KEY','ANALYSIS_KEY'], axis=1)
sonar_issues_complete = pd.concat([sonar_issues_complete_1, sonar_issues_complete_2])
# Deleting duplicated rows
sonar_issues_complete = sonar_issues_complete.drop_duplicates()
sonar_issues_complete = sonar_issues_complete.reset_index(drop = True)
#Joining SONAR_ANALYSIS with SONAR_MEASURES
sonar_measures_complete = pd.merge(sonar_measures, sonar_analysis, left_on = "analysis_key", right_on = "ANALYSIS_KEY", how = "inner")
sonar_measures_complete = sonar_measures_complete.drop(["analysis_key","ANALYSIS_KEY"],axis =1)
# Deleting duplicated rows
sonar_measures_complete = sonar_measures_complete.drop_duplicates()
sonar_measures_complete = sonar_measures_complete.reset_index(drop = True)
sonar_issues_complete = change_commits_to_authors(sonar_issues_complete,"REVISION",commit_author_dict)
sonar_measures_complete = change_commits_to_authors(sonar_measures_complete,"REVISION",commit_author_dict)
# Once both tables contain the author info, we proceeed to aggrupate by such value.

# SONAR_ISSUES 
# First we add a new dummy column containg all 1s that will allow us to compute the total number of issues per author afterwards.
sonar_issues_complete["N_ISSUES"] = [1 for i in range(len(sonar_issues_complete))]
# Then, a dictionary is created indicating which aggregation function will be used for each column.
# In general, the mean will be used except for variables referencing counts.
issues_ag_fun = {}
for col in sonar_issues_complete.select_dtypes(include=dtypes_num).columns:
    issues_ag_fun[col] = 'mean'
counts = ["MESSAGE","BLOCKER","CRITICAL","INFO","MAJOR","MINOR","N_ISSUES"]
for col in counts:
    issues_ag_fun[col] = 'sum'
# Then, the number of differents projects for an authors is also added.
issues_ag_fun["PROJECT_ID"] = 'nunique'
sonar_issues_grouped = sonar_issues_complete.groupby('Author').agg(issues_ag_fun)
sonar_issues_grouped = sonar_issues_grouped.rename(columns={"PROJECT_ID":"N_PROJECTS_I"})
# Then, we perform the same operation for the sonar measures table.

# SONAR_MEASURES
# First we add a new dummy column containg all 1s that will allow us to compute the total number of measures per author afterwards.
sonar_measures_complete["N_MEASURES"] = [1 for i in range(len(sonar_measures_complete))]
# Then, a dictionary is created indicating which aggregation function will be used for each column.
# In general, the mean will be used except for variables referencing counts.
measures_ag_fun = {}
for col in sonar_measures_complete.select_dtypes(include=dtypes_num).columns:
    measures_ag_fun[col] = 'mean'
measures_ag_fun["N_MEASURES"] = 'sum'
# Then, the number of differents projects for an authors is also added.
measures_ag_fun["PROJECT_ID"] = 'nunique'
sonar_measures_grouped = sonar_measures_complete.groupby('Author').agg(measures_ag_fun)
sonar_measures_grouped = sonar_measures_grouped.rename(columns={"PROJECT_ID":"N_PROJECTS_M"})
# Then, the merge between the two tables is executed.
sonar_complete_grouped = sonar_measures_grouped.join(sonar_issues_grouped, how='left')
# As a left join has been performed, the NA values represent authors that have been analyzed but no issues
# where found on such analysis, thus those NA are in reality 0.
sonar_complete_grouped=sonar_complete_grouped.fillna(0)
track("Finishing joining SONAR tables")

# Now, we will proceed with the commit tables.
track("Starting joining COMMIT tables")
# First, we join the git_commits with the git_commit_changes table.
git_complete =  pd.merge(git_commits, git_commits_changes, left_on='COMMIT_HASH', right_on='COMMIT_HASH', how='inner')
git_complete = git_complete.drop("COMMIT_HASH", axis = 1)

# First we add a new dummy column containg all 1s that will allow us to compute the total number of commits with changes per author afterwards.
git_complete["N_COMMITS"] = [1 for i in range(len(git_complete))]

# Then, a dictionary is created indicating which aggregation function will be used for each column.
# In general, the mean will be used except for variables referencing counts.
commits_ag_fun = {}
for col in git_complete.select_dtypes(include=dtypes_num).columns:
    commits_ag_fun[col] = 'mean'

# Then, the number of differents projects for an authors is also added.
commits_ag_fun["PROJECT_ID"] = 'nunique'
commits_ag_fun["N_COMMITS"] = 'sum'
# Regarding the timezone, the most frequent one (in case an author has multiple ones) is added.
commits_ag_fun["AUTHOR_TIMEZONE"] = lambda x:x.value_counts().index[0]

git_complete_grouped = git_complete.groupby('AUTHOR').agg(commits_ag_fun)
git_complete_grouped = git_complete_grouped.rename(columns={"PROJECT_ID":"N_PROJECTS_C"})
git_complete_grouped["AUTHOR_TIMEZONE"] = git_complete_grouped['AUTHOR_TIMEZONE']/3600

# Then, the merge between the sonar and the commits author tables is performed.
complete_table = git_complete_grouped.join(sonar_complete_grouped, how = 'inner')

# We proceed to to delete the variables that only have one value.
for col in complete_table.columns:
    if len(complete_table[col].unique()) == 1:
        complete_table = complete_table.drop(col,axis = 1)

# Lastly, we convert all column names to lowercase and the final dataframe is written in the suitable folder.
#complete_table.to_csv("../../data/processed/model_data.csv")
new_col_names = []
for col in complete_table.columns:
    new_col_names.append(col.lower())
complete_table.columns = new_col_names
try: os.mkdir("../../temp_data/")
except: pass
complete_table.to_csv("../../temp_data/model_data.csv", index_label = "author")


