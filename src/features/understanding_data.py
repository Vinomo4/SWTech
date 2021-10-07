def describe_variables(dataframe, numerical,table):
    '''
    Objective:
        - Obtain a stadistical summary of the variables
    Input:
        - Dataframe : Table with the selected columns
        - Numerical : Numerical types
        - Table : String name of the table 
    Output: 
        For continuous variables:
            - Count : Number of non-null observations
            - Mean : Mean of values
            - Std : Standard Deviation of the Values
            - min : Minimum Value
            - Max : Maximum Value
            - Percentiles 25%,50%,75%
        For categorical variables:
            - Count : Number of non-null observations
            - Unique : Number of classes
            - Top : Class that has more ocurrences
            - req : Ocurrences of the top class
    '''
    dataframe_cont = dataframe.select_dtypes(include=numerical)
    dataframe_cat = dataframe.select_dtypes(exclude=numerical)
    
    cont_empty = dataframe_cont.empty
    cat_empty = dataframe_cat.empty
    
    if not cont_empty and not cat_empty:
        summary_cat = dataframe_cat.describe()
        save_outputs(summary_cat,"summary_cat",None,table)
        summary_cont = dataframe_cont.describe()
        save_outputs(summary_cont,"summary_cont",None,table)

    elif cont_empty and not cat_empty:
        summary_cat = dataframe_cat.describe()
        save_outputs(summary_cat,"summary_cat",None,table)

    elif not cont_empty and cat_empty:
        summary_cont = dataframe_cont.describe()
        save_outputs(summary_cont,"summary_cont",None,table)

    else:
        assert 'The dataframe is empty!'