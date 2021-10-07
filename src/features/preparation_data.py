import pandas as pd
from prettytable import PrettyTable

def delete_na(dataframes, dtypes):
    '''
    Objective:
        - Delete all NA's from the dataframe passed
    Input:
        - Dataframe : String of the tables and their selected columns
        - Numerical : Numerical types

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
        for j in range(len(variable_names)):
            table.add_row([table_names[i], variable_names[j], len(dataframes[i][variable_names[j]].unique()), dataframes[i][variable_names[j]].unique()])
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
        - Generate a column containgthe length of different messages and delete the column
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
