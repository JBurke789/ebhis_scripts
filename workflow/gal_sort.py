import csv
""" 
First code in workflow to run. Runs through csv file of galaxy candidates, and sorts them into 4 catagories. Each catagory has its own csv file with the galaxies.
"""
#create empty csv files to save results from sorting in 
with open('/users/jburke/ebhis_scripts/workflow_results/auto_analyse.csv','w') as empty_csv:
    pass
with open('/users/jburke/ebhis_scripts/workflow_results/outside_vel.csv','w') as empty_csv:
    pass
with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','w') as empty_csv:
    pass
with open('/users/jburke/ebhis_scripts/workflow_results/no_linewidth.csv','w') as empty_csv:
    pass

#go through input candidate list and sort into relevant csv files
with open('/users/jburke/Desktop/gal_candidates_big.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:#looks at each galaxy
        if ' ' in row[0]:
            row[0] = row[0].replace(' ','')
        if row[6]!= '':#has 50pc linewidth
            low_lim  =float(row[3])-float(row[6])-10
            high_lim =float(row[3])+float(row[6])+10
            #Galaxies out of velocity range >+/-605km/s
            if high_lim >= 605 or low_lim<=-605:
                print(row[0], ' outside velocity range')
                with open('/users/jburke/ebhis_scripts/workflow_results/outside_vel.csv','a')as file:
                    write= csv.writer(file)
                    write.writerow(row)
            else:
                #galaxy is ok to automatically gen mom0 maps
                if low_lim>= 50 and high_lim>=50:
                    print(row[0], ' ok to automatically analyse')
                    with open('/users/jburke/ebhis_scripts/workflow_results/auto_analyse.csv','a')as file:
                        write= csv.writer(file)
                        write.writerow(row)
                elif low_lim<=-50 and high_lim<-50:
                    print(row[0], ' ok to automatically analyse')
                    with open('/users/jburke/ebhis_scripts/workflow_results/auto_analyse.csv','a')as file:
                        write= csv.writer(file)
                        write.writerow(row)
                #galaxy is mixed with MW
                else:
                    print(row[0], ' mixed with MW emmision')
                    with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','a')as file:
                        write= csv.writer(file)
                        write.writerow(row)
        #galaxies with no linewidth
        else:
            print(row[0], 'has no linewidth')
            with open('/users/jburke/ebhis_scripts/workflow_results/no_linewidth.csv','a')as file:
                write= csv.writer(file)
                write.writerow(row)

