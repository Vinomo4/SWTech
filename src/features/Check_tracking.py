
# Check if everything works fine
"""
with open('../../reports/tracking/track.txt') as f:
    if '-------------------------DATA UNDERSTANDING-------------------------' in f.read():
        if '-------------------------DATA PREPARATION-------------------------' in f.read():
            if '-------------------------CLUSTERING-------------------------' in f.read():
                if '-------------------------DECISION TREE CLASSIFIER-------------------------' in f.read():
                    if '-------------------------VALIDATION-------------------------' in f.read():
                        print("Everything works fine")
                    else:
                        print("VALIDATION step has not been executed")
                else:
                    print("DECISION TREE CLASSIFIER step has not been executed")
            else:
                print("CLUSTERING step has not been executed")
        else:
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
