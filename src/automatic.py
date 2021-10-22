import os

# install the necesary libraries to run the script

# Define path with .py codes containing functions used in this script
os.getcwd()
#print(os.getcwd())
os.chdir( './features/')
#exec(open("Data_Understanding.py").read())

os.chdir( './features/')
#exec(open("Data_Preparation.py").read())

#os.chdir( '../models/')
#exec(open("Models.py").read())

#os.chdir( '../models/')
#exec(open("validation.py").read())



# Check if everything works fine
with open('../../reports/tracking/track.txt') as f:
    if '-------------------------DATA UNDERSTANDING-------------------------' in f.read():
        if '-------------------------DATA PREPARATION-------------------------' in f.read():
            if '-------------------------CLUSTERING-------------------------' in f.read():
                if '-------------------------VALIDATION-------------------------' in f.read():
                    print("Everything works fine")
                else:
                    print("Validation step has not been executed")
            else:
                print("CLUSTERING and deployment steps have not been executed")
        else:
            print("DATA PREPARATION, CLUSTERING and deployment steps have not been executed")  
    else:
        print("DATA UNDERSTANDING, DATA PREPARATION, CLUSTERING and deployment steps have not been executed")