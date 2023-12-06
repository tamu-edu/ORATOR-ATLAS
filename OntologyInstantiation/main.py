from owlready2 import *
import time
import json
import os
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    
    #parameters
    #input_ATLAS_ontology="../ATLAS_OWL/ATLAS_v2.0.3.owl"
    #input_image_json_directory = "../Datasets/Rellis_3D_image_example/img_json/"
    #input_ontology_mapping= "../Mappings_OWL/RELLIS3D.json"
    #output_owl_directory = "../Datasets/Rellis_3D_image_example/img_owl/"

    
    #GOOSE parameters
    input_ATLAS_ontology="../ATLAS_OWL/ATLAS_v2.0.3.owl"
    input_image_json_directory = "../Datasets/Goose_image_example/img_json/"
    input_ontology_mapping= "../Mappings_OWL/GOOSE.json"
    output_owl_directory = "../Datasets/Goose_image_example/img_owl/"    
    
    
    #start of main code 
    f1 = open(input_ontology_mapping)
    jsonMapping = json.load(f1)
    count = 0
    dict_mapping = {}

    for i in jsonMapping['Class']:
        dict_mapping[i['type']] = count
        count = count + 1


    #list files in input_image_json_directory
    file_list_json=[]
    file_list_owl=[]
    for file in os.listdir(input_image_json_directory):
        if file.endswith(".json"):
            temp_file_json=os.path.join(input_image_json_directory, file)
            #print(temp_file_json)
            file_list_json.append(temp_file_json)
            temp_file_owl=os.path.join(output_owl_directory, file[:-5]+".owl")
            file_list_owl.append(temp_file_owl)
            #print(temp_file_owl)

    print("starting conversion")


    owl_count=-1
    for input_image_json in file_list_json:
        
        #set output owl filename
        owl_count=owl_count+1
        output_owl=file_list_owl[owl_count]

        #load owl ontology
        onto = get_ontology(input_ATLAS_ontology)
        onto.load()

        #load json file from SemanticImage
        f2 = open(input_image_json)
        polygonInfo = json.load(f2)



        count_polygon = 0
        count_terrain = 0

        dict_material = {}
        with onto:

            dict_terrain = {}
            onto.imaging_conditions.ImageDataset = jsonMapping["ImageDataset"]
            onto.instance_ontology.ImageDataset = jsonMapping["ImageDataset"]
            onto.property.ImageDataset = jsonMapping["ImageDataset"]
            temp_val = input_image_json.rfind('/')
            onto.imaging_conditions.ImageName = input_image_json[temp_val+1:-5]
            onto.instance_ontology.ImageName = input_image_json[temp_val+1:-5]
            onto.property.ImageName = input_image_json[temp_val+1:-5]

            for i in polygonInfo['entities']:
                class_instance = i['type']
                if class_instance != 'Ballpark':
                    properties = i["properties"]
                    if class_instance != "unknown_error":
                        idx = dict_mapping[class_instance]
                        poly_type = jsonMapping['Class'][idx]['polygon_instantiation']
                        terrain_type = jsonMapping['Class'][idx]['terrain_instantiation']
                    else:
                        poly_type = "null"
                        terrain_type = ""

                    poly_instance_name = 'F' + str(properties['entity_number'])
                    ind1 = onto[poly_type](poly_instance_name)


                    onto[poly_instance_name].Size = [(properties['pixel_area'])]

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


            onto.save(file=output_owl, format="rdfxml")
            onto.destroy()
            del polygonInfo
            
        
    print("finished conversion")






