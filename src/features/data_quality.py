import os
import numpy as np
from datetime import datetime

def initialize_doc(filename,dataset_name):
    '''
    Objective:
        - Create/empty a document that will store the quality analysis results of a table
          and introduce the different test that will be performed.
    Input:
        - filename : Name of file that will be created.
        - dataset_name: Name of the dataset from which we want to create the document.
    Output:
        - String containing the quality test that will be performed for the selected table.
    '''
    # First, we create the folder where the results will be stored.
    path = '../../reports/figures/data_understanding/data_quality/'
    if not os.path.isdir(path):
        os.makedirs(path)
    # Then we create the intro for the desired dataset.
    title= "-"*10 + " " + dataset_name + " quality analysis " + "-"*10
    title = title.upper()
    title_and_summary = '\n'.join([title,"\n","The test(s) that will be performed for the "+dataset_name.upper()+" table are:"])
    separator = "--------------------------------------------------------------------------------"
    if dataset_name == "Sonar measures": tests = '\n · '.join(["Foreign key constraint","Presence of NAs","Duplicated rows"])
    elif dataset_name == "Sonar issues": tests = '\n · '.join(["Presence of NAs","Duplicated rows"])
    elif dataset_name == "Sonar analysis": tests = '\n · '.join(["Primary key constraint","Foreign key constraint","Duplicated rows"])
    elif dataset_name == "Jira issues": tests = '\n · '.join(['Foreign key constraint',"Number of authors of interest"])
    elif dataset_name == "Git commits": tests = '\n · '.join(["Primary key constraint","Date range of commits","Number of missing authors","Duplicated rows"])
    elif dataset_name == "Git commits changes": tests = '\n · '.join(["Date range of commits","Foreign key constraint","Presence of NAs","Duplicated rows"])
    elif dataset_name == "Szz fault inducing commits": tests = "Number of authors of interest"
    elif dataset_name == "Refactoring miner": tests = "Number of authors of interest"
    intro = '\n · '.join([title_and_summary,tests + "\n"+ separator])
    # Finally the intro is written into the file.
    f = open(path+filename, "w")
    f.write(intro)
    f.close()
    return intro

def write_test_results(filename,test_name,results):
    '''
    Objective:
        - Append the results of a certain quality test into the pertinent file.
    Input:
        - filename : Name of file to apend the results.
        - test_name: Name of the quality test from which the results are.
        - results: Results obtained from test.
    Output:
        - String containing a well-formated presentation of the results from the quality test.
    '''
    path = '../../reports/figures/data_understanding/data_quality/'
    title= "\n"+ "#"*10 + " " + test_name + " test results "+ "#"*10
    title = title.upper()
    separator = "-"*40
    if test_name == "FK":
        if len(results[1]) == 0:
            test_results = '\n · '.join([title,results[0] + "\n"+ separator])
        else:
            results[1] = list(filter(None, results[1]))
            fk_txt = " The FK without references are:" + "\n[" + ','.join(results[1]) + "]"
            test_results = '\n · '.join([title,results[0], fk_txt + "\n"+ separator])
    else:
        test_results = '\n · '.join([title,results + "\n"+ separator])
    f = open(path+filename,"a")
    f.write(test_results)
    f.close()
    return test_results

def write_extra_info(filename,test_name,result,intro):
    '''
    Objective:
        - Append information about the extra test performed to certain tables to their specific file.
    Input:
        - filename : Name of file to apend the extra info.
        - test_name: Name of the performed test.
        - result: Result of the extra test.
        - intro: Brief explanation on why and what test was performed.
    Output:
        - None.
    '''
    path = '../../reports/figures/data_understanding/data_quality/'
    # Writting the intro in the doc.
    f = open(path+filename,"a")
    f.write("\n"+intro)
    f.close()
    print(intro)
    print(write_test_results(filename,test_name,result),end = "")



def check_PK(dataset,pk):
    '''
    Objective:
        - Evaluate if a table has repeated/missing values in the Primary Key variable.
    Input:
        - dataset : Pandas dataset that wants to be analyzed (One table of the TechDebt DS).
        - pk : Name of the Primary Key of the table.
   Output:
    For tables without NA problems:
        - String indicating that there isn't any problem.
    For tables with NA problems:
        - String containg the percentage of repeated values.
    '''
    if len(dataset[pk].unique()) != len(dataset):
        result = "There are "+ str(round((len(dataset)-len(dataset[pk].unique()))/len(dataset)*100,4)) + "% rows with a non-unique PK value."
    else: result = "All the PK are unique."
    return result

def check_NAs(dataset,columns_of_interest):
    '''
    Objective:
        - Evaluate if a table has missing values in a subset of columns.
    Input:
        - dataset : Pandas dataset that wants to be analyzed (One table of the TechDebt DS).
        - columns_of_interest : Names of the columns to be checked.
    Output:
        For tables without NA problems:
            - String indicating that there aren't any missing values.
        For tables with NA problems:
            - String containg the columns with missing values and their percentage.
            - List with the same info than the string.

    '''
    cols_with_NA = [(col,dataset[col].isna().sum()/len(dataset[col])*100) for col in columns_of_interest if dataset[col].isna().sum() > 0]
    if len(cols_with_NA) != 0:
        result = "The columns that contain NAs are:\n" + '\n'.join(" "*6+x[0]+" → "+str(round(x[1],4))+"%" for x in cols_with_NA)
    else: result = "There aren't NAs in the table."
    return result,cols_with_NA

def check_missing_authors(dataset,column):
    '''
    Objective:
        - Evaluate if a table has missing authors in the given column.
    Input:
        - dataset : Pandas dataset that wants to be analyzed (One table of the TechDebt DS).
        - column : Names of the columns that contains the authors.
    Output:
        For tables without missing authors problems:
            - String indicating that there aren't any missing values.
        For tables with missing authors problems:
            - String containg the percentage of missing values.
    '''
    no_authors = sum(dataset[column] == "No Author") + sum(dataset[column].isna())
    if no_authors != 0:
        result = "The percentage of missing authors is:" + str(round(no_authors/len(dataset)*100,3))+"%."
    else: result("All the rows contain an author.")
    return result


def check_dates(dataset,column,ub,lb,date_format):
    '''
    Objective:
        - Evaluate if a all the values of a column that contain dates are between an upper and a lower bound.
          (The dates are in 'YYYY-mm-ddTHH:MM:SSZ' format).
    Input:
        - dataset : Pandas dataset that wants to be analyzed (One table of the TechDebt DS).
        - column : Column name that contain the dates.
        - ub: Upper bound for the dates (Datetime object).
        - lb: Year lower bound for the dates (in string format).
        -date_format: Index indicating whether a space or "T" calendar-hour separation is used.
    Output:
        For tables without range problems:
            - String indicating that there isn't any problem.
        For tables with range problems:
            - String indicating the percentage of dates outside the range.
    '''
    aux = dataset.dropna()
    if date_format == 1:
        date_style = "%Y-%m-%dT%H:%M:%SZ"
    else: date_style = "%Y-%m-%d %H:%M:%S"
    if min(aux[column]).split("-")[0] < lb or datetime.strptime(max(aux[column]).split("+")[0],date_style) > ub:
        out_range = len(aux[(aux[column].split("-")[0] < lb) | (datetime.strptime(aux[column],"%Y-%m-%dT%H:%M:%SZ") >ub)])
        result = "There are "+str(round(out_range/len(dataset)*100,3))+ "date outside the specified range."
    else: result = "All the dates are in the specified range."
    return result


def check_FK(dataset,fk,dataset_w_pk,pk):
    '''
    Objective:
        - Evaluate if a table has a foreign key that don't reference any primary key from another table.
    Input:
        - dataset : Pandas dataset that wants to be analyzed (One table of the TechDebt DS).
        - fk : Name of the Foreign Key from the table.
        - dataset_w_pk: Pandas dataset that contains the values referenced in the FK of "dataset".
        - pk: Name of the Primary Key of "dataset_w_pk".
    Output:
        For tables without FK problems:
            - String indicating that there isn't any problem.
            - An empty list
        For tables with NA problems:
            - String inidicating the percentage of FK violations.
            - List of all the fk that aren't referenced.

    '''
    pks_list = list(dataset_w_pk[pk].unique())
    fk_violations = [x for x in list(dataset[fk].unique()) if x not in pks_list]
    if len(fk_violations) != 0:
        result = str(round(len(fk_violations)/len(dataset)*100,3)) + "% of the FKs are unreferenced."
    else: result = "All the FK values have an associated PK."
    return result,fk_violations

def check_duplicates(dataset):
    '''
    Objective:
        - Evaluate if a table has duplicated rows.
    Input:
        - dataset : Pandas dataset that wants to be analyzed (One table of the TechDebt DS).
    Output:
        For tables without duplicated problems:
            - String indicating that there isn't any problem.
        For tables with duplicated problems:
            - String inidicating the percentage of duplicatd rows.
    '''
    num_duplicated = dataset.duplicated().sum()
    if not num_duplicated:
        result = "There aren't any duplicated rows."
    else: result = "There are " + str(round(num_duplicated/len(dataset)*100,3)) + " % of duplicated rows."
    return result

def check_matching(ref_set,table,column):
    '''
    Objective:
        - Compute the number of unique elements that are present on the provided checklist
        for an specific column of a dataframe.
    Input:
        - ref_list: Set containg the reference values of interest.
        - table : Dataframe that wants to be used.
        - column : Name of the variable that contains the values to check.
    Output:
        For columns with all matching values:
            - String indicating that there isn't any problem.
        For columns with non-matching values:
            - String indicating the number of elements that match and the percentatge regarding the
            length of "ref_list"
    '''
    col_vals = set(table[column])
    num_matching = len(col_vals.intersection(ref_set))
    if num_matching == len(col_vals):
        result = "The table contains inforation about all authors of interest."
    else:
        result = "There are " + str(num_matching) +" authors of interest, which represents the " +str(round(num_matching/len(ref_set)*100,4)) + " % from the total authors of interest"
    return result
