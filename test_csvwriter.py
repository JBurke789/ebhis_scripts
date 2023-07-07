import csv
name='Galaxy1'

with open('/users/jburke/ebhis_scripts/values.csv','r') as file:
    s=file.read()
    newline = ['Galaxy1,','val1,','val2']
    if name not in s:
          with open('/users/jburke/ebhis_scripts/values.csv','a') as f:
                f.writelines(newline)
          
          
                   
                
