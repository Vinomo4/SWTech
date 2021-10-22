import os
# Posar fitxer d'instalar llibreries
# Define path with .py codes containing functions used in this script
#os.getcwd()
print(os.getcwd())
os.chdir( './features/')
#exec(open("Data_Understanding.py").read())

#exec(open("Data_Preparation.py").read())
os.chdir( '../models/')
exec(open("Models.py").read())
os.chdir( '../models/')
#exec(open("validation.py").read())