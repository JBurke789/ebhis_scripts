import csv

'''
makes a region to mark the location of each galaxy in casa
'''



with open('/users/jburke/ebhis_scripts/workflow_results/need_manual_analysis.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        file1 =  row[0]+'/location.crtf'
        with open(file1,'w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n',
                      'ellipse [[',row[1],'deg,',row[2],'deg], [800arcsec, 800arcsec], 0.00000000deg],label="',row[0],'"']
            file.write(''.join(lines))
