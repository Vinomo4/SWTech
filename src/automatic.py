import os
# Posar fitxer d'instalar llibreries
# Define path with .py codes containing functions used in this script
#os.getcwd()
os.chdir( './features/')
print(os.getcwd())
exec(open("Data_Understanding.py").read())
