import pandas as pd
import numpy as np
from prettytable import PrettyTable

def delete_na(dataframes, dtypes):
    '''
    Objective:
        - Delete all NA's from the dataframes passed
    Input:
        - dataframes : String of the tables and their selected columns
        - dtypes : Numerical types

    Output:
        - Dataframe with the deleted values.
    '''
    for i in range(len(dataframes)):
        dataframe_numerical = dataframes[i].select_dtypes(include=dtypes)
        total_rows = dataframe_numerical.shape[0]
        # Delete rows that contain na's
        dataframe_numerical = dataframe_numerical.dropna()
        dataframes[i] = dataframe_numerical
    return dataframes

def analyse_categorical_variables(table_names, variable_names, dataframes):
    '''
    Objective:
        - Analyse the categorical variables to be encoded
    Input:
        - Table_names : String of the names of the tables
        - Variable_names : String of the categorical variables corresponding to the table
        - Dataframes : String of the tables and their selected columns

    Output:
        - Table with the categorical variables levels
        ["Table name", "Variable name", "Number of levels", "Types"]
    '''
    table = PrettyTable()
    table.field_names = ["Table name", "Variable name", "Number of levels", "Types"]
    for i in range(len(table_names)):
        for j in range(len(variable_names[i])):
            table.add_row([table_names[i], variable_names[i][j], len(dataframes[i][variable_names[i][j]].unique()), dataframes[i][variable_names[i][j]].unique()])
    print(table)

def one_hot_encoding(table, variable):
    '''
    Objective:
        - Encode the categorical variable passed from the table to one-hot encoding.
          If the categorical variable only has one level, the column is deleted.
    Input:
        - Table : String of the table name
        - Variable : String of the categorical variable corresponding to the table

    Output:
        For categorical variables with more than one level:
            - Table with the categorical variable encoded to one-hot
            ["Table name", "Variable name", "Number of levels", "Types"]
        For categorical variables with less than one level:
            -String indicating so.
    '''
    # The column contain more than one level.
    if len(table[variable].unique()) > 1:
        variable_dummies = pd.get_dummies(table[variable])
        table = table.drop(variable, axis=1)
        table = table.join(variable_dummies)
        return table
    # The column contain only one value and will be deleted.
    else:
        return table.drop(variable, axis=1)

def message_length(table,column):
    '''
    Objective:
        - Generate a column containg the length of different messages and delete the column
          that contains the orignal text.
    Input:
        - table : Dataframe that wants to be used.
        - column : Name of the variable that contains the messages.
    Output:
        - None
    '''
    message_length = []
    for msg in table[column]:
        message_length.append(len(msg))
    # Reassign the MESSAGE variable to its length instead of the initial string \n",
    table[column] = message_length


def change_commits_to_authors(table,column,author_dict):
    '''
    Objective:
        - Generate a column containg the authors of a respective analysis/issue
          instead of the FK commit reference.
    Input:
        - table : Dataframe that wants to be used.
        - column : Name of the variable that contains the commits.
        - author_dict: Dictionary containg commits as key an its author as value.
    Output:
        - Dataframe containg the mentioned modification.
    '''
    authors_measures = []
    for i in range(len(table)):
        aux = table[column][i]
        if author_dict.get(aux): authors_measures.append(author_dict[aux])
        else: authors_measures.append(np.nan)

    # Then, we add the column to the sonar_complete table and delete the REVISION one.

    table["Author"] = authors_measures
    table = table.drop(column,axis=1)
    return table
