import csv

'''
run in full galaxy list directory
'''

def command_line(name):
    in_path = name +'/no_filter_moment0'
    out_path = '/users/jburke/Desktop/results/moment0_maps/'+name+'.jpg'

    imview(raster={'file': in_path, 
                   'colorwedge':True     },
                   zoom=2,
                   out=out_path
                   )

with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for i in reader:
        command_line(i[0])
        print(i[0])