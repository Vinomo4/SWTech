# Import libraries and packages
import os
import matplotlib.pyplot as plt

os.getcwd()
os.chdir( '../features')
from tracking import track

def save_plot(fig,filename):
    '''
    Objective:
        - Save plots
    Input:
        - fig: figure we want to save
        - filename: Name of the file 
    Output:
        - None
    '''

    # Path and name of the file/figure we want to save
    path = '../../reports/figures/validation'+"/"
    file_name = path+"/"+filename+".png"
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
        plt.savefig(file_name, transparent=True)
    else:
        plt.savefig(file_name, transparent=True)
    track("Successfully saved %s" % path)

def plot_quality_metrics(df, metrics, yticks):
    '''
    Objective:
        - To plot the metric values for each cluster
    Input:
        - df: dataframe 
        - metrics: selected columns of the dataframe to be plotted
        - yticks: y-axis values to be printed in the plot
    Output:
        - Plot: plots the metric values for each cluster to compare among them
    '''
    FONTSIZE = 27
    FIG_WIDTH = 30
    FIG_HEIGHT = 10
    fgr = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    for metric in metrics:
        markers, caps, bars = plt.errorbar(range(len(df)), df[metric + '_mean'], df[metric + '_std'],
                                        label=metric,  fmt='--o', markersize=12, elinewidth=4)
        [bar.set_alpha(0.4) for bar in bars]
        [cap.set_alpha(0.4) for cap in caps]

    plt.title('Quality of each cluster', fontsize = FONTSIZE)
    plt.xlabel('Cluster', fontsize = FONTSIZE)
    plt.ylabel('Metric value', fontsize = FONTSIZE)
    plt.xticks(ticks=range(len(df)), labels=df["clusters"], fontsize = FONTSIZE)
    plt.yticks(ticks = yticks, fontsize=FONTSIZE)
    if metrics[0] == "blocker_violations":
        legend_metrics = ["Blocker violations", "Critical violations", "Major violations", "Minor violations"]
    elif metrics[0] == "blocker":
        legend_metrics = ["Blocker severity issues", "Critical severity issues", "Major severity issues", "Minor severity issues"]
    else: 
        legend_metrics = ["Code smells", "Bugs" "Vulnerabilities"]
    plt.legend(legend_metrics, bbox_to_anchor=(1.001,0.8), prop={'size': FONTSIZE})
    plt.grid()
    if metrics[0] == "blocker_violations":
        save_plot(fgr, "violations")
    elif metrics[0] == "blocker":
        save_plot(fgr, "severity_issues")
    else: 
        save_plot(fgr, "issues_types")
    plt.close()