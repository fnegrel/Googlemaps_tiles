# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:37:46 2017

@author: FLOLT
"""

#Libs import
import urllib.request as url
import numpy as np
from PIL import Image
import csv
import getpass


#Definition of variable
#NWlat = input("Latitude Coords for the NW corner:")
#NWlong = input("Longitude Coords for the NW corner:")
#SElat = input("Latitude Coords for the SE corner:")
#SElong = input("Longitude Coords for the SE corner:")
#c = csv.writer(open("Images/manifest2.csv",dialect='excel',"w",newline=''),delimiter=',')

    
    
name = ""
user = getpass.getuser()


#Get and crop your googlemaps image !
def cropping():
    compt = 0
    data= [["subject_id","image_name","origin","link","attribution","license"]]
    #Definition of the bounding of the area
    #NW = [float(NWlat),float(NWlong)]
    #50SE = [float(SElat),float(SElong)]
    
    #Testing area
    NW=[26.919206, 75.879581]
    SE=[26.872678, 75.972613]
    
    #Get the size of the area in lat & long
        #largeur 100m = 0.0009
    height = NW[0]-SE[0] 
        #longueur 100m = 0.0018
    width = SE[1]-NW[1]  
    
    #Definition of "gap" for the cropping, 80% of new element by image here, x et y are number of rows and columns for the crop
    x=np.linspace(NW[0],SE[0],height/(0.0009*4))
    y=np.linspace(SE[1],NW[1],width/(0.0018*4))
    
    
    
    #Double loop to fetch the subimage
    for i in range(len(y)-1):
        for j in range(len(x)-1):
            a = (x[i]+x[i+1])/2
            b = (y[j]+y[j+1])/2
            compt = compt+1
            #Request to get the corresponding image on the google map API
            response = url.urlopen("https://maps.googleapis.com/maps/api/staticmap?center="+str(a)+","+str(b)+"&zoom=16&size=800x400&scale=2&maptype=satellite&format=jpg&key=AIzaSyBBW23KLCKQ7tTUaCZ7Eu-7CZLLfcj5wnw")
            #Use of PIL lib to make the treatment on the image
            Image_see = Image.open(response)
            #Saving each image on the disk
            name = "Area_"+str(i)+"_"+str(j)
            Image_see.save("Images/Area_"+str(i)+"_"+str(j)+".jpg")
            response.close()  
                        
            data = data + [[compt, name, 'GoogleMapsAPI', 'https://maps.googleapis.com/maps/api/staticmap?center='+str(a)+','+str(b)+'&zoom=16&size=800x400&scale=2&maptype=satellite&format=jpg&key=AIzaSyBBW23KLCKQ7tTUaCZ7Eu-7CZLLfcj5wnw', user, 'Creative Commons - share adapt attribute']]
    #Writing the manifest for zooniverse        
    outfile = open('Images/Manifest.csv', 'w')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    writer.writerows(data)
    outfile.close()
    return("done")

if __name__=='__main__':

    cropping()