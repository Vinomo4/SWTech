# Import libraries and packages
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
sys.path.append('../features/')

from tracking import track
from fun_classifiers import train_decision_tree,train_random_forest

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
        plt.savefig(file_name)
    else:
        plt.savefig(file_name)
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
    FONTSIZE = 12
    FIG_WIDTH = 12
    FIG_HEIGHT = 7
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
    plt.tight_layout()

    if metrics[0] == "blocker_violations":
        legend_metrics = ["Blocker violations", "Critical violations", "Major violations", "Minor violations"]
    elif metrics[0] == "blocker":
        legend_metrics = ["Blocker severity issues", "Critical severity issues", "Major severity issues", "Minor severity issues"]
    else:
        legend_metrics = ["Code smells", "Bugs", "Vulnerabilities"]
    plt.legend(legend_metrics, bbox_to_anchor=(1.001,0.8), prop={'size': FONTSIZE})
    plt.grid()
    if metrics[0] == "blocker_violations":
        save_plot(fgr, "violations")
    elif metrics[0] == "blocker":
        save_plot(fgr, "severity_issues")
    else:
        save_plot(fgr, "issues_types")
    plt.close()

def compare_classifiers(data, part_size):
    '''
    Objective:
        - Generate a line chart where the x axis represents the depth of the tree
          and the y-axis the test accuracy for both DT/RF classifiers.
    Input:
        - data: Dataframe that contains the values used for modeling
        - part_size: Percentage of values reserved for testing.
    Output:
        - The plot itself.
    '''
    # Aesthetic theme selection
    plt.style.use('ggplot')
    # Droping undesired columns
    data = data.drop(["author", "quality_rating"],axis = 1)
    dt_accs = []
    rf_accs = []
    # Path for storing the plot.
    path = '../../reports/figures/validation/'
    if not os.path.isdir(path):
        os.makedirs(path)
    for i in range(3,10):
        _,_,dtc_acc,_ = train_decision_tree(data,part_size, depth = i,plot = False)
        _,_,rf_acc,_ = train_random_forest(data,part_size,depth = i)
        dt_accs.append(dtc_acc)
        rf_accs.append(rf_acc)
    # plotting DT points
    plt.plot(range(3,10), dt_accs, label = "DT")
    # plotting RF points
    plt.plot(range(3,10), rf_accs, label = "RF")
    plt.xlabel('Tree(s) maximum depth')
    plt.ylabel('Test accuracy')
    plt.title('Comparison of perfomance between DT/RF')
    plt.legend()
    plt.savefig(path+"classifier_comparison.png")
    plt.close()
