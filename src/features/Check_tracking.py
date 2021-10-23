
# Check if everything works fine
with open('../../reports/tracking/track.txt') as f:
    if '-------------------------DATA UNDERSTANDING-------------------------' in f.read():
        if '-------------------------DATA PREPARATION-------------------------' in f.read():
            if '-------------------------CLUSTERING-------------------------' in f.read():
                if '-------------------------DECISION TREE CLASSIFIER-------------------------' in f.read():
                    if '-------------------------VALIDATION-------------------------' in f.read():
                        if '-------------------------DEPLOYMENT-------------------------' in f.read():
                            print("Everything works fine")
                        else:
                            print("DEPLOYMENT step has not been executed") 
                    else:
                        print("VALIDATION and DEPLOYMENT steps have not been executed")
                else:
                    print("DECISION TREE CLASSIFIER, VALIDATION and DEPLOYMENT steps have not been executed")
            else:
                print("CLUSTERING, DECISION TREE CLASSIFIER, VALIDATION and DEPLOYMENT steps have not been executed")
        else:
            print("DATA PREPARATION, CLUSTERING , DECISION TREE CLASSIFIER, VALIDATION and DEPLOYMENT steps have not been executed")  
    else:
        print("DATA UNDERSTANDING, DATA PREPARATION, CLUSTERING , DECISION TREE CLASSIFIER, VALIDATION and DEPLOYMENT steps have not been executed")