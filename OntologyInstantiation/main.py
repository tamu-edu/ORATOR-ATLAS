# This is a sample Python script.
from owlready2 import *
import time
import json

import matplotlib.pyplot as plt
import numpy as np


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    f = open('C:/Users/anant/Desktop/ATLAS_ontology/pythonScript/JSON files/Class2OntologyMapping.json')
    jsonMapping = json.load(f)

    f = open('C:/Users/anant/Desktop/ATLAS_ontology/pythonScript/JSON files/segmented_output_240.json')
    polygonInfo = json.load(f)

    onto = get_ontology("C:/Users/anant/Desktop/ATLAS_ontology/pythonScript/ATLAS_v2.0.3.owl")

    onto.load()
    print("start")
    tic = time.perf_counter()

    count = 0
    dict_mapping = {}
    for i in jsonMapping['Class']:
        dict_mapping[i['type']] = count
        count = count + 1
        #i["terrain_instantiation"])

    count_polygon = 0
    count_terrain = 0

    dict_material = {}
    with onto:

        # onto.save(file = "inferSaveRDF.owl", format = "rdfxml")
        #fencesubc = list(onto.fence.subclasses())
        dict_terrain = {}
        onto.imaging_conditions.ImageDataset = jsonMapping["ImageDataset"]
        onto.instance_ontology.ImageDataset = jsonMapping["ImageDataset"]
        onto.property.ImageDataset = jsonMapping["ImageDataset"]

        for i in polygonInfo['entities']:
            class_instance = i['type']
            #if class_instance != 'Ballpark'  and class_instance != 'rock' and class_instance != 'leaves':
            if class_instance != 'Ballpark':
                properties = i["properties"]
                idx = dict_mapping[class_instance]
                poly_type = jsonMapping['Class'][idx]['polygon_instantiation']
                terrain_type = jsonMapping['Class'][idx]['terrain_instantiation']

                poly_instance_name = 'F' + str(properties['entity_number'])
                ind1 = onto[poly_type](poly_instance_name)

                onto[poly_instance_name].Size = [properties['pixel_area']]

                if terrain_type != '':
                    if terrain_type in dict_material.keys():
                        terrain_instance_name = dict_material[terrain_type]
                        ind2 = onto[terrain_instance_name]
                    else:
                        count_terrain = count_terrain + 1
                        terrain_instance_name = 'M' + str(count_terrain)
                        dict_material[terrain_type] = terrain_instance_name
                        ind2 = onto[terrain_type](terrain_instance_name)
                    ind1.HasMaterial.append(ind2)


        onto.save(file="img1_ontology.owl", format="rdfxml")





