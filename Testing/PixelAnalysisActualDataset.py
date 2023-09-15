from owlready2 import *
import time
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime


if __name__ == '__main__':
    # Find no of pixels in each semantic class from JSON files
    input_image_json_directory = "../Datasets/Rellis_3D_image_example/img_json/"
    input_ontology_mapping = "../Mappings_OWL/RELLIS3D.json"

    # start of main code
    f1 = open(input_ontology_mapping)
    jsonMapping = json.load(f1)
    pixelCount = {}
    for i in jsonMapping['Class']:
        pixelCount[i['type']] = 0

    # list files in input_image_json_directory
    file_list_json = []
    for file in os.listdir(input_image_json_directory):
        if file.endswith(".json"):
            temp_file_json = os.path.join(input_image_json_directory, file)
            # print(temp_file_json)
            file_list_json.append(temp_file_json)
            # print(temp_file_owl)

    print("starting conversion")

    owl_count = -1
    for input_image_json in file_list_json:
        # load json file from SemanticImage
        f2 = open(input_image_json)
        polygonInfo = json.load(f2)

        for i in polygonInfo['entities']:
            class_instance = i['type']
            if class_instance != 'Ballpark':
                properties = i["properties"]
                pixelCount[class_instance] = pixelCount[class_instance] + int(properties['pixel_area'])


    print(pixelCount)
    print("finished conversion")


    # Find no of pixels in each semantic c;ass from OWL files
    #parameters
    # input_ontology_mapping= "../Mappings_OWL/RELLIS3D.json"
    # # input_owl_directory = "E:/datasets/OWL_datasets/a2d2/"
    # input_owl_directory = "../Datasets/Rellis_3D_image_example/img_owl/"
    #
    # start_time = time.time()
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    #
    # file_list_owl = []
    # for file in os.listdir(input_owl_directory):
    #     if file.endswith(".owl"):
    #         temp_file_owl = os.path.join(input_owl_directory, file)
    #         file_list_owl.append(temp_file_owl)
    #         # print(temp_file_owl)
    #
    # #start of main code
    # f1 = open(input_ontology_mapping)
    # jsonMapping = json.load(f1)
    # dict_mapping = {}
    # pixelCount = {}
    #
    # for i in jsonMapping['Class']:
    #     poly_type = i['polygon_instantiation']
    #     terrain_type = i['terrain_instantiation']
    #     dict_mapping[i['type']] = [poly_type ,terrain_type ]
    #     pixelCount[i['type']] = 0
    #
    # print("starting conversion")
    #
    #
    # for input_owl in file_list_owl:
    #     #load owl ontology
    #     onto = get_ontology(input_owl)
    #     onto.load()
    #     listIndividuals = list(onto.individuals())
    #     for i in listIndividuals:
    #         ins_type = i.is_a[0].name
    #         ins_mat = ''
    #         if i.HasMaterial:
    #             ins_mat = i.HasMaterial[0].is_a[0].name
    #
    #         for ele in dict_mapping:
    #             if ins_type == dict_mapping[ele][0] and ins_mat == dict_mapping[ele][1]:
    #                 if i.Size:
    #                     pixelCount[ele] = pixelCount[ele] + int(i.Size[0])
    #
    # owl_count=-1
    # print("finished conversion")

