
# Check if everything works fine
"""
with open('../../reports/tracking/track.txt') as f:
<<<<<<< HEAD
    if '-------------------------DATA UNDERSTANDING-------------------------' in f.read():
        if '-------------------------DATA PREPARATION-------------------------' in f.read():
            if '-------------------------CLUSTERING-------------------------' in f.read():
                if '-------------------------DECISION TREE CLASSIFIER-------------------------' in f.read():
                    if '-------------------------VALIDATION-------------------------' in f.read():
                        print("Everything works fine")
=======
    if "-"*25 + "DATA UNDERSTANDING" + "-"*25 in f.read():
        if "-"*25 + "DATA PREPARATION" + "-"*25 in f.read():
            if "-"*25 + "CLUSTERING" + "-"*25 in f.read():
                if "-"*25 + "DECISION TREE CLASSIFIER" + "-"*25 in f.read():
                    if "-"*25 + "VALIDATION" + "-"*25 in f.read():
                            print("Everything works fine")
>>>>>>> 6fb659da62d033fcd3cb94ed8eb6b5e26e8ee57a
                    else:
                        print("VALIDATION step has not been executed")
                else:
                    print("DECISION TREE CLASSIFIER step has not been executed")
            else:
                print("CLUSTERING step has not been executed")
        else:
<<<<<<< HEAD
            print("DATA PREPARATION step has not been executed")  
    else:
        print("DATA UNDERSTANDING step has not been executed")

"""

# Check if everything works fine
All_fine = True

with open('../../reports/tracking/track.txt') as f:
    if not '-------------------------DATA UNDERSTANDING-------------------------' in f.read():
        print("DATA UNDERSTANDING step has not been executed")
        All_fine = False

with open('../../reports/tracking/track.txt') as f:
    if not '-------------------------DATA PREPARATION-------------------------' in f.read():
        print("DATA PREPARATION step has not been executed")
        All_fine = False

with open('../../reports/tracking/track.txt') as f:
    if not '-------------------------CLUSTERING-------------------------' in f.read():
        print("CLUSTERING step has not been executed")
        All_fine = False

with open('../../reports/tracking/track.txt') as f:
    if not '-------------------------DECISION TREE CLASSIFIER-------------------------' in f.read():
        print("DECISION TREE CLASSIFIER step has not been executed")
        All_fine = False

with open('../../reports/tracking/track.txt') as f:
    if not '-------------------------VALIDATION-------------------------' in f.read():
        print("VALIDATION step has not been executed")
        All_fine = False

if All_fine:
    print("Everything works fine")
=======
            print("DATA PREPARATION, CLUSTERING , DECISION TREE CLASSIFIER, and VALIDATION steps have not been executed")
    else:
        print("DATA UNDERSTANDING, DATA PREPARATION, CLUSTERING , DECISION TREE CLASSIFIER, and VALIDATION steps have not been executed")
>>>>>>> 6fb659da62d033fcd3cb94ed8eb6b5e26e8ee57a
