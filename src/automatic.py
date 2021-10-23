import os

# Define path with .py codes containing functions used in this script
os.getcwd()
#print(os.getcwd())
os.chdir( './features/')
#exec(open("Data_Understanding.py").read())

os.chdir( '../data/')
print(os.getcwd())
exec(open("Data_Preparation.py").read())

#os.chdir( '../models/')
#exec(open("Models.py").read())

#os.chdir( '../models/')
#exec(open("Decision Tree Classifier.py").read())

#os.chdir( '../models/')
#exec(open("validation.py").read())

# Check if everything works fine
os.chdir( './features/')
exec(open("Check_tracking.py").read())
