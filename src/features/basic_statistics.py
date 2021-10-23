import os
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sn

from tracking import track


def save_outputs(fig,type_plot,variable,name_table):
    '''
    Objective:
        - Save png figures or csv files
    Input:
        - Fig : figure or file that want to be saved
        - Type_plot : Barplot/histogram/heatmap/summary_cont/summary_cat/type_variables
        - Variable : Name of the table variable or None
        - Name_table : String name of the table
    Output:
        - None
    '''
    # Path to store text.
    path_txt = '../../reports/texts/data_understanding'
    # Path to store images.
    path_img = '../../reports/figures/data_understanding'
    # Path and name of the file/figure we want to save
    if variable == None :
        if type_plot == 'summary_cont' or type_plot == 'summary_cat':
            path = path_txt+"/"+type_plot[0:7]+"/"+name_table
            file_name = path+"/"+type_plot+".csv"
        else:
            if type_plot == "type_variables":
                path = path_txt+"/"+type_plot+"/"+name_table
                file_name = path+"/"+type_plot+".csv"
            else :
                path = path_img+"/"+type_plot+"/"+name_table
                file_name = path+"/"+type_plot+".png"
    else:
        path = path_img+"/"+type_plot+"/"+name_table
        file_name = path+"/"+type_plot+"_"+variable+".png"

    # Directory creation if doesn't exists
    try:
        os.makedirs(path)
    except OSError:
        pass
    else:
        track("Successfully created the directory %s" % path)

    # Save the figure/file
    if (os.path.exists(file_name)== True):
        track ("Warning: Figure %s already created" % path)
        track('Figure will be overwritten')
        #c = input('  Do you want to overwrite content?(y/n)')
        #if c.lower() == 'n':
        #    print('Figure will not be overwritten, no action done')
        #    return
        if type_plot == 'summary_cont' or type_plot == 'summary_cat' or type_plot == "type_variables":
            fig.to_csv(file_name)
        else:
            plt.savefig(file_name)
    else:
        if type_plot == 'summary_cont' or type_plot == 'summary_cat' or type_plot == "type_variables":
            fig.to_csv(file_name)
        else:
            plt.savefig(file_name)

        track("Successfully saved %s" % path)

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

def bar_plot(variable,dataframe,vertical,name_table):
    '''
    Objective:
        - Obtain a barplot of a variable
    Input:
        - Variable : data of the variable we want want to plot
        - Dataframe : All the table
        - Vertical : Is we want to plot the bar chart vertical (True) or horizontal(False)
        - Name_table : String name of the table

    Output:
        - Barplot
    '''
    labels = variable.unique()
    count = np.zeros(len(labels))

    for i in range(len(labels)):
        count[i] = dataframe[variable== labels[i]].count()[0]
    if vertical:
        fig = plt.barh(labels,count)
        plt.ylabel(variable.name)
        plt.xlabel('Count')
    else:
        fig = plt.bar(labels,count)
        plt.xlabel(variable.name)
        plt.ylabel('Count')

    plt.title('Data of each '+variable.name)
    save_outputs(fig,'barplot',variable.name,name_table)


def plot_histogram(dataframe,numerical,name_table):
    '''
    Objective:
        - Plot a histogram of all numeric variables in dataframe
    Input:
        - Dataframe : Table with the selected columns
        - Numerical : Numerical types
        - Name_table : String name of the table
    Output:
        - Histogram
    '''
    dataframe = dataframe.select_dtypes(include=numerical)
    if dataframe.empty:
        track(f'There are no numerical variables in dataframe')
    else:
        for col in dataframe.columns:
            fig = plt.hist(x=dataframe[col], color='#F2AB6D', rwidth=0.85)
            fig = plt.title(f'{col} histogram')
            fig = plt.xlabel(f'{col}')
            fig = plt.ylabel('Frequency')
            save_outputs(fig,'histogram',col,name_table)


def plot_correlations(dataframe, numerical,name_table):
    '''
    Objective:
        - Plot a heatmap of all numeric variables in dataframe
    Input:
        - Dataframe : Table with the selected columns
        - Numerical : Numerical types
        - Name_table : String name of the table
    Output:
        - Heatmap
    '''

    dataframe = dataframe.select_dtypes(include=numerical)
    if dataframe.empty:
        track(f'There are no numerical variables in dataframe')
    else:
        corrMatrix = dataframe.corr()
        if name_table == "sonar_measures":
            plt.figure(figsize = (20,20))
        fig = sn.heatmap(corrMatrix, annot=True)
        save_outputs(fig,'heatmap',None,name_table)
