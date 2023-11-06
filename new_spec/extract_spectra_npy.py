import csv
import numpy as np
"""
runs through csv and extracts spectra from casa files and saves as numpy file
run in casa 
source /vol/software/software/astro/casa/initcasa.sh
"""
def extract_spectra(name):
    ia.open(name+'/raw_image.im')
    ON_flux = ia.getregion(name+'/man_spec_ON.crtf')
    OFF_flux = ia.getregion(name+'/man_spec_OFF.crtf')
    ia.close()
    ON_temp = np.sum(np.sum(ON_flux,axis=0),axis=0)
    OFF_temp = np.sum(np.sum(OFF_flux,axis=0),axis=0)
    ia.open(name+'/hanning_smoothed1.im')
    ON_flux = ia.getregion(name+'/man_spec_ON.crtf')
    OFF_flux = ia.getregion(name+'/man_spec_OFF.crtf')
    ia.close()
    ON_h1_temp = np.sum(np.sum(ON_flux,axis=0),axis=0)
    OFF_h1_temp = np.sum(np.sum(OFF_flux,axis=0),axis=0)
    ia.open(name+'/hanning_smoothed2.im')
    ON_flux = ia.getregion(name+'/man_spec_ON.crtf')
    OFF_flux = ia.getregion(name+'/man_spec_OFF.crtf')
    ia.close()
    ON_h2_temp = np.sum(np.sum(ON_flux,axis=0),axis=0)
    OFF_h2_temp = np.sum(np.sum(OFF_flux,axis=0),axis=0)
    ia.open(name+'/hanning_smoothed3.im')
    ON_flux = ia.getregion(name+'/man_spec_ON.crtf')
    OFF_flux = ia.getregion(name+'/man_spec_OFF.crtf')
    ia.close()
    ON_h3_temp = np.sum(np.sum(ON_flux,axis=0),axis=0)
    OFF_h3_temp = np.sum(np.sum(OFF_flux,axis=0),axis=0)
    ia.open(name+'/hanning_smoothed4.im')
    ON_flux = ia.getregion(name+'/man_spec_ON.crtf')
    OFF_flux = ia.getregion(name+'/man_spec_OFF.crtf')
    ia.close()
    ON_h4_temp = np.sum(np.sum(ON_flux,axis=0),axis=0)
    OFF_h4_temp = np.sum(np.sum(OFF_flux,axis=0),axis=0)

    statsON = imstat(imagename=name+'/raw_image.im',
                    region =name+'/man_spec_ON.crtf')
    statsOFF = imstat(imagename=name+'/raw_image.im',
                    region =name+'/man_spec_OFF.crtf')
    statsON_h1 = imstat(imagename=name+'/hanning_smoothed1.im',
                    region =name+'/man_spec_ON.crtf')
    statsOFF_h1 = imstat(imagename=name+'/hanning_smoothed1.im',
                    region =name+'/man_spec_OFF.crtf')
    statsON_h2 = imstat(imagename=name+'/hanning_smoothed2.im',
                    region =name+'/man_spec_ON.crtf')
    statsOFF_h2 = imstat(imagename=name+'/hanning_smoothed2.im',
                    region =name+'/man_spec_OFF.crtf')
    statsON_h3 = imstat(imagename=name+'/hanning_smoothed3.im',
                    region =name+'/man_spec_ON.crtf')
    statsOFF_h3 = imstat(imagename=name+'/hanning_smoothed3.im',
                    region =name+'/man_spec_OFF.crtf')
    statsON_h4 = imstat(imagename=name+'/hanning_smoothed4.im',
                    region =name+'/man_spec_ON.crtf')
    statsOFF_h4 = imstat(imagename=name+'/hanning_smoothed4.im',
                    region =name+'/man_spec_OFF.crtf')
    
    OFF_temp_norm = (OFF_temp/float(statsOFF['npts']))*float(statsON['npts'])
    OFF_temp_h1_norm =(OFF_h1_temp/float(statsOFF_h1['npts']))*float(statsON_h1['npts'])
    OFF_temp_h2_norm =(OFF_h2_temp/float(statsOFF_h2['npts']))*float(statsON_h2['npts'])
    OFF_temp_h3_norm =(OFF_h3_temp/float(statsOFF_h3['npts']))*float(statsON_h3['npts'])
    OFF_temp_h4_norm =(OFF_h4_temp/float(statsOFF_h4['npts']))*float(statsON_h4['npts'])

    return ON_temp,ON_h1_temp,ON_h2_temp,ON_h3_temp,ON_h4_temp,OFF_temp_norm,OFF_temp_h1_norm,OFF_temp_h2_norm,OFF_temp_h3_norm,OFF_temp_h4_norm

def get_vel(name,temp_in,image):
  ia.open(name+image)
  csys=ia.coordsys()
  x=np.array(np.arange(0,len(temp_in),1.)) #need floating point array
  freqs = copy.deepcopy(x)
  velo=copy.deepcopy(x)
  blctemp=[0,0,0]
  for a in range(0,len(x)):
    blctemp[2]=x[a]
    w=ia.toworld(blctemp,'n')
    freq=w['numeric'][2] # gives frequencies
    v=csys.frequencytovelocity(value=freq,doppler='radio',velunit='km/s')
    velo[a]=float(v)
  return velo

def unit_conversion(temp):
  flux_jy = temp/1.28
  flux_BA = flux_jy/8.64
  return flux_BA

def save_npy(name , vel,flux_ON,flux_OFF,filename):
   output = np.stack((vel,flux_ON,flux_OFF),axis=0)
   np.save(name+filename,output)

with open('/users/jburke/ebhis_scripts/catagorisation/cat_results/MW_overlap.csv','r') as f:
   reader = csv.reader(f)
   header = next(reader)
   for row in reader:
        name = row[0]

        ON_temp,ON_h1_temp,ON_h2_temp,ON_h3_temp,ON_h4_temp,OFF_temp_norm,OFF_temp_h1_norm,OFF_temp_h2_norm,OFF_temp_h3_norm,OFF_temp_h4_norm=extract_spectra(name)

        ON_flux = unit_conversion(ON_temp)
        OFF_flux = unit_conversion(OFF_temp_norm)
        vels = get_vel(name,ON_temp,'/raw_image.im')
        save_npy(name,vels,ON_flux,OFF_flux,'/man_spec_h0.npy')

        ON_flux = unit_conversion(ON_h1_temp)
        OFF_flux = unit_conversion(OFF_temp_h1_norm)
        vels = get_vel(name,ON_h1_temp,'/hanning_smoothed1.im')
        save_npy(name,vels,ON_flux,OFF_flux,'/man_spec_h1.npy')

        ON_flux = unit_conversion(ON_h2_temp)
        OFF_flux = unit_conversion(OFF_temp_h2_norm)
        vels = get_vel(name,ON_h2_temp,'/hanning_smoothed2.im')
        save_npy(name,vels,ON_flux,OFF_flux,'/man_spec_h2.npy')

        ON_flux = unit_conversion(ON_h3_temp)
        OFF_flux = unit_conversion(OFF_temp_h3_norm)
        vels = get_vel(name,ON_h3_temp,'/hanning_smoothed3.im')
        save_npy(name,vels,ON_flux,OFF_flux,'/man_spec_h3.npy')

        ON_flux = unit_conversion(ON_h4_temp)
        OFF_flux = unit_conversion(OFF_temp_h4_norm)
        vels = get_vel(name,ON_h4_temp,'/hanning_smoothed4.im')
        save_npy(name,vels,ON_flux,OFF_flux,'/man_spec_h4.npy')


   
