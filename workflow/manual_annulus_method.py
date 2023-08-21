import csv 
import os
import numpy as np

class galaxy:
    def __init__(self,row):
        self.row= row
        self.name=row[0]
        self.ra = row[1]
        self.dec = row[2]
        self.dist = row[3]
        self.radvel = row[4]
        self.mag21 = row[5]
        self.w50 = row[6]

    def region_vals(self):
        map_name = self.name+'/no_filter_moment0'
        imview(map_name)
        gal_vis = input('Is galaxy visible: (y/n) ')
        if gal_vis == 'n':
            with open('/users/jburke/ebhis_scripts/workflow_results/cant_analyse.csv','a') as file:
                write= csv.writer(file)
                write.writerow(row)
        else: 
            in_sum = float(input('Inner sum: '))
            in_npix = float(input('Inner npix: '))
            #in_rms =  float(input('Inner rms: '))
            out_sum = float(input('Outer sum: ')) 
            out_npix = float(input('Outer npix: '))
            #out_rms =  float(input('Outer rms: '))
            #bg_rms = np.sqrt((out_npix/(out_npix-in_npix))*(out_rms**2 - (in_npix/(out_npix))*in_rms**2))
            bg_rms = 0.09# rms=90mK from ebhis calibration
            #calculates flux from values in annuli
            bg_flux = out_sum-in_sum
            bg_npix = out_npix-in_npix
            bg_per_pix = bg_flux/bg_npix
            clean_flux = in_sum - bg_per_pix*in_npix
            flux_jy = clean_flux/1.28
            norm_flux_jy = flux_jy/8.64
            uncert = bg_rms*np.sqrt(in_npix)
            frac_uncert = uncert/clean_flux
            norm_uncert = frac_uncert*norm_flux_jy 
            print('background rms = '+str(bg_rms))
            print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(norm_uncert))
            setattr(self,'norm_flux',norm_flux_jy)
            setattr(self,'norm_flux_uncert',norm_uncert)

#looks for csv file to store gals that can't be analysed, makes one if not there
csvpath = '/users/jburke/ebhis_scripts/workflow_results/cant_analyse.csv'
if not os.path.exists(csvpath):
    with open('/users/jburke/Desktop/test_gal_list.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        with open('/users/jburke/ebhis_scripts/workflow_results/cant_analyse.csv','w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
else:
    pass

#makes a list of all galaxy names that have been analysed
galaxies_analysed =[]
with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        name = row[0]
        galaxies_analysed.append(name)
with open('/users/jburke/ebhis_scripts/workflow_results/cant_analyse.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        name = row[0]
        galaxies_analysed.append(name)





with open('/users/jburke/ebhis_scripts/workflow_results/need_manual_analysis.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print('...')
        print(row[0])
        print('...')
        if row[0] in galaxies_analysed:
            print(str(row[0])+' already analysed')
        else:
            obj=galaxy(row)
            obj.region_vals()
            #save results?
            save = input('Save results?: (y/n) ')
            if save == 'y':
                file1 = '/users/jburke/ebhis_scripts/workflow_results/final_results.csv'
                note=input('Note:')
                with open(file1,'a') as file:
                    a= obj.norm_flux
                    b=obj.norm_flux_uncert
                    lines = [obj.name,
                            obj.ra,
                            obj.dec,
                            obj.dist,
                            obj.radvel,
                            obj.mag21,
                            obj.w50,
                            str(a),
                            str(b),
                            str(note),
                            '\n']
                    file.write(','.join(lines))
            else:
                print(obj.name,' not saved')