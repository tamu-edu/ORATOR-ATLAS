from owlready2 import *
import time
import json

import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    
    input_ontology_mapping= "json/RELLIS3D.json"
    input_image_json = "json/segmented_output_240.json"
    input_ATLAS_ontology="ATLAS_v2.0.3.owl"


    f1 = open(input_ontology_mapping)
    jsonMapping = json.load(f1)

    f2 = open(input_image_json)
    polygonInfo = json.load(f2)

    onto = get_ontology(input_ATLAS_ontology)

    onto.load()
    print("starting conversion")
    tic = time.perf_counter()

    count = 0
    dict_mapping = {}
    for i in jsonMapping['Class']:
        dict_mapping[i['type']] = count
        count = count + 1

    count_polygon = 0
    count_terrain = 0

    dict_material = {}
    with onto:

        dict_terrain = {}
        onto.imaging_conditions.ImageDataset = jsonMapping["ImageDataset"]
        onto.instance_ontology.ImageDataset = jsonMapping["ImageDataset"]
        onto.property.ImageDataset = jsonMapping["ImageDataset"]

        for i in polygonInfo['entities']:
            class_instance = i['type']
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
        print("finished conversion")






