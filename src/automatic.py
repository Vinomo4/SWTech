import os

# Define path with .py codes containing functions used in this script

#os.chdir( './features/')
#exec(open("Data_Understanding.py").read())

os.chdir( '../data/')
#exec(open("Data_Preparation.py").read())

print()
os.chdir( '../models/')
exec(open("Clustering.py").read())

#exec(open("Decision Tree Classifier.py").read())

os.chdir( '../models/')
exec(open("Validation.py").read())

# Check if everything works fine
#os.chdir( '../features/')
#exec(open("Check_tracking.py").read())
