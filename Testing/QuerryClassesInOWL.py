from owlready2 import *
import time
import json
import os
import tkinter as tk
from tkinter import simpledialog

if __name__ == '__main__':

    #parameters
    input_owl_directory = "Datasets/freiburg/img_owl/"
    # input_owl_directory = "../OWL_files/rugd/"
    owl_mappings_directory = "Mappings_OWL/"
    print('input directory',input_owl_directory)
    
    #start of main script
    list_files = [] #list of files which have the requested class
    file_list_owl=[]
    for file in os.listdir(input_owl_directory):
        if file.endswith(".owl"):
            temp_file_owl=os.path.join(input_owl_directory, file)
            file_list_owl.append(temp_file_owl)
            # print(temp_file_owl)

    file_list_mappings = []
    dict_mapping = {}
    pixelMinArea = 1000
    print('pixelMinArea: ', pixelMinArea)
    for file in os.listdir(owl_mappings_directory):
        if file.endswith(".json"):
            temp_file_mappings = os.path.join(owl_mappings_directory, file)
            file_list_mappings.append(temp_file_mappings)
            f1 = open(temp_file_mappings)
            jsonMapping = json.load(f1)
            # print(1)
            for i in jsonMapping['Class']:
                if i['type'] not in dict_mapping:
                    dict_mapping[i['type'].lower()] = [i['polygon_instantiation'], i['terrain_instantiation']]

    ## Creating GUI to take input from user
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    classOfInterest = simpledialog.askstring(title="Search",
                                      prompt="What semantic class images do you want to extract?:")
    classOfInterest = classOfInterest.lower()
    print('class of interes', classOfInterest)
    for input_owl in file_list_owl:
        #load owl ontology
        onto = get_ontology(input_owl)
        onto.load()

        imageName = onto.scenario_labels.ImageName
        imageDataset = onto.scenario_labels.DatasetName

        if onto[classOfInterest]:
            # print("Ontology Hierarchy")
            ontoClassOfInterest = onto[classOfInterest]
            if ontoClassOfInterest.instances():
                # print("Found")
                for k in list(ontoClassOfInterest.instances()):
                    if k.SizeArea:
                        if int(k.SizeArea[0]) > pixelMinArea:
                            list_files.append([imageName[0], imageDataset[0]])
                            break
                    else:
                        sz_n = 0
                        for j in list(k.Makes):
                            sz_n = sz_n + int(j.SizeArea[0])

                        if sz_n > pixelMinArea:
                            list_files.append([imageName[0], imageDataset[0]])
                            break
               # list_files.append([imageName[0], imageDataset[0]])
            # else:
            #     print("Not Found")

        elif classOfInterest in dict_mapping:
            # print("From some dataset")

            if dict_mapping[classOfInterest][1]!= '':
                ontoClassOfInterestP = onto[dict_mapping[classOfInterest][0]]
                ontoClassOfInterestM_I = onto[dict_mapping[classOfInterest][1]].instances()
                counter = 0
                for inst in ontoClassOfInterestP.instances():
                    if inst.HasMaterial == ontoClassOfInterestM_I and int(inst.SizeArea[0]) > pixelMinArea:
                        # print("Found")
                        list_files.append([imageName[0], imageDataset[0]])
                        counter = 1
                        break
                if counter == 0:
                    print("Not Found")

            else:
                ontoClassOfInterest = onto[dict_mapping[classOfInterest][0]]
                if ontoClassOfInterest.instances():
                    # print("Found")
                    for k in list(ontoClassOfInterest.instances()):
                        if k.SizeArea:
                            if int(k.SizeArea[0]) > pixelMinArea:
                                list_files.append([imageName[0], imageDataset[0]])
                                break

                    # list_files.append([imageName[0], imageDataset[0]])
                # else:
                #     print("Not Found")

        # else:
        #     print("Not Found")


        onto.destroy()

    if list_files:
        # print(list_files)
        print('number of images', len(list_files))
    else:
        print("Not Found", classOfInterest)
    print("done")