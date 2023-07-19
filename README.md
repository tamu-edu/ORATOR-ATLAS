# ORATOR-ATLAS
This repo holds the relevant code for an All-Terrain Labelset for Autonomous Systems (ATLAS) developed by the Off-Road Annotation TOols & Resources (ORATOR) team and Texas A&M Univsity. The goal of this effort is to develop a standardized ontology for off-road datasets to unify exisiting and future dataset ontologies. This standardized ontological framework can be used to aid training AI-models on data that is collected from multiple datasets. Moreover, the integration of W3C Web Ontology Language (OWL) allows for easy addition to the proposed ontology and the ability to analyze data for inconsistencies. 

## Supported Datasets 
The mappings from current datasets to ATLAS has been created for:

- RELLIS3D

The converted datasets are available upon request. 


## Installation 

The installation dependencies are divided into relevant parts. This is to reflect the different parts of the proposed pipeline. 

The installation instructions assume that the development platform is Ubuntu 20.04. 

### Dependencies for SemanticImage

SemanticImage relies on 2 dependencies - OpenCV and jsoncpp. Jsoncpp and CMake can be installed with the below command: 

`sudo apt-get install cmake libjsoncpp-dev`

#### Install  OpenCV:
The process for installing the most recent version of OpenCV with the contrib modules is:

`cd ~`

`mkdir opencv_build`

`cd opencv_build`


`wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip`

`wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip`

`unzip opencv.zip`

`unzip opencv_contrib.zip`

`mkdir -p build && cd build`

`cmake -DOPENCV_ENABLE_NONFREE:BOOL=ON  -DOPENCV_EXTRA_MODULES_PATH=/home/$USER/opencv_build/opencv_contrib-4.x/modules /home/$USER/opencv_build/opencv-4.x/     -D OPENCV_GENERATE_PKGCONFIG=ON `

`make -j$(nproc)`

`sudo make install`

### Dependencies for OntologyInstantiation

The dependencies for OnotologyInstantiation can be installed by the below command:


`sudo apt install python3-pip  `


` pip install owlready2 numpy matplotlib `


### W3C Web Ontology Language (OWL) - Protege

OWL is used to represent the ontology in a hierarchical manner and leverage open-source packages for analyzing and modifying ATLAS. OWL allows us to take ATLAS one step further from the previous version and allow objects to have the ability to have multiple parents and assign properties to individual objects. This facilitates the addition of context to images and objects. Moreover, there are tools that can be used to determine if labellers assign inconsistent labels or properties to an object.

The recommended software package to use is Protege. The link to Protege can be found [here](https://protege.stanford.edu/). It is recommended to install Protege  Desktop. This application allows for viewing and modifying the onotology. 

The onotology can be loaded into the software by .....

## SemanticImage 
This package is used to start the conversion of existing semantically segmented datasets into a more standarized format. The input to this step is a semantically segmented image and a json file containing the RGB value and corresponding semantic class. The output file contains the necessary information for input into OntologyInstantiation, such as the input image, ATLAS version, object class, object size, and polygon vertices.


### Parameters: 
**input_image** - This is the name of the input image for analysis. 

**input_json** - This input json should contain the semantic class and corresponding RGB value for the dataset being analyzed. 

**output_json** - The output json is the name of the file that is to be written after analysis.  

**num_threads** - This is the number of threads that can be used to help speed up processing times. The default is to use all threads on the machine. 

**min_polygon_area** - This is the minimum number of pixels that a contour needs or else it is filtered out and not outputted to the output json file. 

**ATLAS_version** - This is the current version of ATLAS being used. The default is "2.1.2". This is one of the items included in the json file. 

### Usage
Make sure to adjust the parameters to match your setup. Make sure you are in the main directory for the ORATOR-ATLAS repo. After the code can be built and run by the following commands in the terminal:

`cd SemanticImage`

`mkdir build`

`cd build`

`cmake ..`

`make`

`./main`

After the initial time, the code only needs to be rebuilt after changes are made to the the corresponding files. The code can be rebuilt by the following command. Make sure that you are in the build directory for this SemanticImage. 

`make`

After the code is built, the code can be run by the following command. Make sure that you are in the build directory for SemanticImage. 

`./main`

## OntologyInstantiation 

This package is used to take the json file from SemanticImage and convert it to a unified ATLAS ontology. 

### Parameters

**input_ontology_mapping** - This is a file that converts the semantic classes from an existing dataset into the ATLAS ontology. 

**input_image_json** - This is the output file from SemanticImage. 

**input_ATLAS_ontology** - This is the OWL file for the ATLAS version being used. 

### Usage 

From the OntologyInstantiation directory, the code can be run with:

`python3 main.py`

## Acknowledgements
This work is a collaboration between USARMY GVSC and TAMU. 


## TO-DO
- Need to generate visualization images
- Installation instructions for gtk 
- Automate the process for a directory instead of single  image and output should correspond to input name 
- Update list of supported datasets
- Example integration showing the distribution of objects/images for single dataset and multidataset
- Example integration showing the images from different datasets in a unified ontology