import numpy as np
import os
import csv
import copy

def make_regions(name,ra,dec):
    #makes central region for ON spectrum and four OFF spectra
    file1 = name +'/center_ON_spectrum.crtf'
    with open(file1,'w') as file:
        lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',ra,'deg,',dec,'deg], [5000arcsec, 5000arcsec], 0.00000000deg]']
        file.write(''.join(lines))
    
    file2 = name+'/OFF_tr_spectrum.crtf'
    tr_ra = str(float(ra)+1.5)
    tr_dec = str(float(dec)+1.5)
    with open(file2,'w') as file:
        lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',tr_ra,'deg,',tr_dec,'deg], [1000arcsec, 1000arcsec], 0.00000000deg]']
        file.write(''.join(lines))

    file3 = name+'/OFF_tl_spectrum.crtf'
    tl_ra = str(float(ra)-1.5)
    tl_dec = str(float(dec)+1.5)
    with open(file3,'w') as file:
        lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',tl_ra,'deg,',tl_dec,'deg], [1000arcsec, 1000arcsec], 0.00000000deg]']
        file.write(''.join(lines))

    file4 = name+'/OFF_bl_spectrum.crtf'
    bl_ra = str(float(ra)-1.5)
    bl_dec = str(float(dec)-1.5)
    with open(file4,'w') as file:
        lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',bl_ra,'deg,',bl_dec,'deg], [1000arcsec, 1000arcsec], 0.00000000deg]']
        file.write(''.join(lines))
    
    file5 = name+'/OFF_br_spectrum.crtf'
    br_ra = str(float(ra)+1.5)
    br_dec = str(float(dec)-1.5)
    with open(file5,'w') as file:
        lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',br_ra,'deg,',br_dec,'deg], [1000arcsec, 1000arcsec], 0.00000000deg]']
        file.write(''.join(lines))

    print("Region files generated for ", name)


def extract_spectra(name):
    ia.open(name+'/raw_image.im')#ON spectrum
    flux = ia.getregion(name+'/center_ON_spectrum.crtf')
    ia.close()
    temp_ON =np.sum(np.sum(flux,axis=0),axis=0)
    ia.open(name+'/raw_image.im')#OFF spectra
    flux = ia.getregion(name+'/OFF_tr_spectrum.crtf')
    ia.close()
    temp_OFF_tr =np.sum(np.sum(flux,axis=0),axis=0)    
    ia.open(name+'/raw_image.im')
    flux = ia.getregion(name+'/OFF_tl_spectrum.crtf')
    ia.close()
    temp_OFF_tl =np.sum(np.sum(flux,axis=0),axis=0)
    ia.open(name+'/raw_image.im')
    flux = ia.getregion(name+'/OFF_bl_spectrum.crtf')
    ia.close()
    temp_OFF_bl =np.sum(np.sum(flux,axis=0),axis=0)
    ia.open(name+'/raw_image.im')
    flux = ia.getregion(name+'/OFF_br_spectrum.crtf')
    ia.close()
    temp_OFF_br =np.sum(np.sum(flux,axis=0),axis=0)



    statsON = imstat(imagename=name+'/raw_image.im',
                    region =name+'/center_ON_spectrum.crtf')
    statsOFFtr = imstat(imagename=name+'/raw_image.im',
                    region =name+'/OFF_tr_spectrum.crtf')
    statsOFFtl = imstat(imagename=name+'/raw_image.im',
                    region =name+'/OFF_tl_spectrum.crtf')
    statsOFFbl = imstat(imagename=name+'/raw_image.im',
                    region =name+'/OFF_bl_spectrum.crtf')
    statsOFFbr = imstat(imagename=name+'/raw_image.im',
                    region =name+'/OFF_br_spectrum.crtf')
    
    bg_temp = temp_OFF_tl+temp_OFF_tr+temp_OFF_bl+temp_OFF_br
    bg_npix = float(statsOFFtr['npts'])+float(statsOFFtl['npts'])+float(statsOFFbl['npts'])+float(statsOFFbr['npts'])
    
    temp_OFF_norm= (bg_temp/bg_npix)*float(statsON['npts']) #background temp scales to same pixels as ON spectrum
    print('Spectra extracted for ', name)
    return temp_ON, temp_OFF_norm


def get_vel(name,temp_in):
    ia.open(name+'/raw_image.im')
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

def save_npy(name,velo,flux_inner,bg_flux_inner):
    output = np.stack((velo,flux_inner,bg_flux_inner),axis=0)
    np.save(name+'/spectrum.npy',output)
    print('Spectra saved in numpy file')

        


name = input('Galaxy name: ')

with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0]== name:
            ra = row[1]
            dec = row[2]
            make_regions(name,ra,dec)
            temp_ON,temp_OFF = extract_spectra(name)
            vel = get_vel(name,temp_ON)
            flux_ON = unit_conversion(temp_ON)
            flux_OFF = unit_conversion(temp_OFF)
            save_npy(name,vel,flux_ON,flux_OFF)


