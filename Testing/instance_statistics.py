from owlready2 import *
import time
import json
import os
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':

    #parameters
    input_owl_directory = "../Datasets/Rellis_3D_image_example/img_owl/"

    
    #start of main script
    
    file_list_owl=[]
    for file in os.listdir(input_owl_directory):
        if file.endswith(".owl"):
            temp_file_owl=os.path.join(input_owl_directory, file)
            file_list_owl.append(temp_file_owl)
            #print(temp_file_owl)

    dictionary_of_materials = {}
    dictionary_of_instances = {}
    dictionary_of_instance_pixels = {}

    for input_owl in file_list_owl:
        #load owl ontology

        onto = get_ontology(input_owl)
        onto.load()


        named_individuals = list(onto.individuals())
        for individual in named_individuals:
            #print(individual.name)  # Print the name of each named individual
            #use this name to get number of instances of each class

            if(individual.name[0]=='M'):
                temp_count=0

            for value in individual.get_properties():
                #print((individual.get_properties())) 
                if (value.python_name=='Size'):
                    for size in value[individual]:
                        #print(individual.is_a[0].name, value.python_name, size) #prints number of pixels for entity
                        # above print example: Sky Size 100.0
                        try:
                            dictionary_of_instance_pixels[individual.is_a[0].name]+=size
                        except:
                            dictionary_of_instance_pixels[individual.is_a[0].name]=size
                elif (value.python_name=='HasMaterial'):
                    pass
                    # for material in value[individual]:
                    #     print(individual.is_a[0].name, value.python_name, material.name)
                    #     # above print example: Sky HasMaterial M1
                elif (value.python_name=='Makes'):
                    for temp in value[individual]:
                        # print(individual.is_a[0].name, value.python_name, temp.name)
                        temp_count=temp_count+1
                        # above print example: Sky Makes F1
                        #can use this to determine quantity of each material 
                else:
                    print('undefine value ',value.python_name )
            if(individual.name[0]=='M'):
                #print(individual.is_a[0].name, "has ", temp_count, " instances")
                try:
                    dictionary_of_materials[individual.is_a[0].name]+=temp_count
                except:
                    dictionary_of_materials[individual.is_a[0].name]=temp_count
            if(individual.name[0]=='F'):
                try:
                    dictionary_of_instances[individual.is_a[0].name]+=1
                except:
                    dictionary_of_instances[individual.is_a[0].name]=1

        onto.destroy()

       
        #print('end of file ------')
        

    print('dataset has the following number of entities for each material \n',dictionary_of_materials)

    print('dataset has the following number of entities for each instance \n',dictionary_of_instances)

    print('dataset has the following number of pixels for each instance \n',dictionary_of_instance_pixels)


    # To do:

    #need to check some of the owl:NamedIndividual 
    # has multiple type and material  for some
    # errors when multiple of same property ie multily type or HasMaterial
    
    # need to think about how nesting works when displaying statistics 

    # need to verify these results by comparison with json files
    # seem like there is double of what is expected


    input_image_json_directory = "../Datasets/Rellis_3D_image_example/img_json/"
    file_list_json=[]
    dictionary_of_json_entitites = {}
    print('verify with json files')
    for file in os.listdir(input_image_json_directory):
        if file.endswith(".json"):
            temp_file_json=os.path.join(input_image_json_directory, file)
            #print(temp_file_json)
            file_list_json.append(temp_file_json)

    for input_image_json in file_list_json:
        f2 = open(input_image_json)
        polygonInfo = json.load(f2)

        for i in polygonInfo['entities']:
            class_instance = i['type']
            # print(class_instance)
            try:
                dictionary_of_json_entitites[class_instance]+=1
            except:
                dictionary_of_json_entitites[class_instance]=1
    print(dictionary_of_json_entitites)


    
