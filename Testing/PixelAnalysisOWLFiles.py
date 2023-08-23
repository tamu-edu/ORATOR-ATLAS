from owlready2 import *
import time
import json
import os
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime


if __name__ == '__main__':

    #parameters
    input_owl_directory = "E:/datasets/OWL_datasets/a2d2/"
    # input_owl_directory = "../Datasets/Rellis_3D_image_example/img_owl/"

    start_time = time.time()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    #start of main script
    file_list_owl=[]

    for file in os.listdir(input_owl_directory):
        if file.endswith(".owl"):
            temp_file_owl=os.path.join(input_owl_directory, file)
            file_list_owl.append(temp_file_owl)
            #print(temp_file_owl)

    counter = 0
    PixelsPerClass_fullDataSet = {}
    print("Number of Images", len(file_list_owl))

    for input_owl in file_list_owl:
        #load owl ontology
        onto = get_ontology(input_owl)
        onto.load()
        counter = counter + 1
        print(counter)
        PixelsPerClass = {}

        imageName = onto.imaging_conditions.ImageName
        imageDataset = onto.imaging_conditions.ImageDataset

        list_classes = list(onto.classes())
        for OntologyClass in list_classes:
            noOfPixels = 0
            for instance in OntologyClass.instances():
                if instance.Size:
                    noOfPixels = noOfPixels + int(instance.Size[0])
                else:
                    for item in instance.Makes:
                        if item.Size:
                            noOfPixels = noOfPixels + int(item.Size[0])

            PixelsPerClass[OntologyClass.name] = noOfPixels
            if OntologyClass.name in PixelsPerClass_fullDataSet:
                PixelsPerClass_fullDataSet[OntologyClass.name] = PixelsPerClass_fullDataSet[OntologyClass.name] + noOfPixels
            else:
                PixelsPerClass_fullDataSet[OntologyClass.name] = noOfPixels
        onto.destroy()

       
    print(PixelsPerClass_fullDataSet)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("done")