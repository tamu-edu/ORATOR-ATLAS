from owlready2 import *
import time
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv



if __name__ == '__main__':

    #parameters
    input_img_json="../Datasets/Rellis_3D_image_example/img_json/frame000000-1581623790_349.json"
    input_color_scheme="../Mappings_RGB/Rellis3D_dataset.json"
    
    
    #start of main script
    f1 = open(input_img_json)
    polygonInfo = json.load(f1)

    f2 = open(input_color_scheme)
    colorInfo = json.load(f2)

    color_dict={}
    for i in colorInfo['Color_Information']:
        
        red_value=colorInfo['Color_Information'][i]['red_value']
        blue_value=colorInfo['Color_Information'][i]['blue_value']
        green_value=colorInfo['Color_Information'][i]['green_value']
        # print(i,red_value,green_value, blue_value)
        color_dict[i]=[blue_value,green_value,red_value]



    for i in polygonInfo['entities']:
        class_instance = i['type']

        #use the ballpark to initialize image size
        if (class_instance=='Ballpark'):
            coordinates=i['geometry']['coordinates']
            #print(coordinates)
            height=int(coordinates[2][1])
            width=int(coordinates[2][0])
            color_image = np.zeros((height,width,3), np.uint8)
            # print(height,width)
        else:
            #get the coordinates
            # print(class_instance)
            coordinates=np.array(i['geometry']['coordinates'])
            # print(coordinates)
            # need to get color scheme for each item 
            color_scheme=color_dict[class_instance]
            # print(color_scheme)
            #create a mask on the blank image and fill it with the color scheme
            # print(coordinates.shape)
            # cv.drawContours(image, contours, -1, (0, 255, 0), 3)
            cv.fillPoly(color_image, pts =[coordinates], color=color_scheme)

            

    #resize color image
    disp_image=cv.resize(color_image,(500,500))
    cv.imshow('test', disp_image)
    cv.waitKey()
    

    #need to create a common color scheme for atlas for display
    #need to show image in atlas color scheme 
           

