
# Check if everything works fine
with open('../../reports/tracking/track.txt') as f:
    if "-"*25 + "DATA UNDERSTANDING" + "-"*25 in f.read():
        if "-"*25 + "DATA PREPARATION" + "-"*25 in f.read():
            if "-"*25 + "CLUSTERING" + "-"*25 in f.read():
                if "-"*25 + "DECISION TREE CLASSIFIER" + "-"*25 in f.read():
                    if "-"*25 + "VALIDATION" + "-"*25 in f.read():
                            print("Everything works fine")
                    else:
                        print("VALIDATION step has not been executed")
                else:
                    print("DECISION TREE CLASSIFIER, and VALIDATION steps have not been executed")
            else:
                print("CLUSTERING, DECISION TREE CLASSIFIER, and VALIDATION steps have not been executed")
        else:
            print("DATA PREPARATION, CLUSTERING , DECISION TREE CLASSIFIER, and VALIDATION steps have not been executed")
    else:
        print("DATA UNDERSTANDING, DATA PREPARATION, CLUSTERING , DECISION TREE CLASSIFIER, and VALIDATION steps have not been executed")
