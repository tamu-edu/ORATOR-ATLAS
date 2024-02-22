from owlready2 import *
import time
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import sys 



if __name__ == '__main__':

    #parameters
    input_color_scheme="Mappings_RGB/unify_dataset_rgb.json"
    
    results_dir = '../classified_images_grey/'
    # input_img_dir = '../semantic_images/' #includes sub directories for each dataset
    input_img_dir = '../extracted_json/' #includes sub directories for each dataset
    # zip file is on google drive for datasets
    
    use_greyscale = True
    
    file_ext = '.json'  
    files_list = os.listdir(input_img_dir)
    input_files = []
    # print(files_list)
    for file in files_list:
        # print(file)
        files_list_subdir = os.listdir(input_img_dir+file+'/')
        for file_subdir in files_list_subdir:
            # print(file_subdir)
            input_img_png=input_img_dir+file+'/'+file_subdir
            _, extension = os.path.splitext(input_img_png)
            if extension == file_ext:
                input_files.append(input_img_png)
                # print(input_img_png)
    # print size of input_files
    # print(len(input_files))
                    
    
        
    #start of main script
    f2 = open(input_color_scheme)
    colorInfo = json.load(f2)

    color_dict={}
    grey_scale_dict={}
    for i in colorInfo['Color_Information']:
        
        red_value=colorInfo['Color_Information'][i]['red_value']
        blue_value=colorInfo['Color_Information'][i]['blue_value']
        green_value=colorInfo['Color_Information'][i]['green_value']
        class_value=colorInfo['Color_Information'][i]['class_value']
        # print(i,red_value,green_value, blue_value)
        color_dict[i]=[blue_value,green_value,red_value]
        grey_scale_dict[i]=class_value
    
    # print(grey_scale_dict)
    # sys.exit()
    
    for input_img_json in input_files:
    
        f1 = open(input_img_json)
        
        
        
        polygonInfo = json.load(f1)

        



        for i in polygonInfo['entities']:
            class_instance = i['type']

            #use the ballpark to initialize image size
            if (class_instance=='Ballpark'):
                coordinates=i['geometry']['coordinates']
                #print(coordinates)
                height=int(coordinates[2][1])
                width=int(coordinates[2][0])
                if (use_greyscale):
                    color_image = np.zeros((height,width,1), np.uint8)
                else:
                    color_image = np.zeros((height,width,3), np.uint8)
                # print(height,width)
            else:
                #get the coordinates
                # print(class_instance)
                coordinates=np.array(i['geometry']['coordinates'])
                # print(coordinates)
                # need to get color scheme for each item 
                if (use_greyscale):
                    color_scheme=int(grey_scale_dict[class_instance])
                else:
                    color_scheme=color_dict[class_instance]
                # print(color_scheme)
                #create a mask on the blank image and fill it with the color scheme
                # print(coordinates.shape)
                # cv.drawContours(image, contours, -1, (0, 255, 0), 3)
                cv.fillPoly(color_image, pts =[coordinates], color=color_scheme)

                

        #resize color image for visualization 
        # disp_image=cv.resize(color_image,(500,500))
        # cv.imshow('test', disp_image)
        # cv.waitKey(1000)
        
        
        # Determine the directory
        dir_path = results_dir + input_img_json.split('/')[-2]

        # Create the directory if it doesn't exist
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Determine the file path
        file_path = dir_path + '/' + input_img_json.split('/')[-1].split('.')[0] + '.png'
        print(file_path)

        # save images 
        cv.imwrite(file_path, color_image)
        # cv.imshow('test', color_image)
        # cv.waitKey(1000)
        
    

   
    print('Done')
