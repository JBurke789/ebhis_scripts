import csv
from collections import Counter

names=[]
with open('/users/jburke/Desktop/results/full_results.csv','r') as f :
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        names.append(row[0])


cnt = Counter(names)
print([k for k,v in cnt.items() if v >1])
