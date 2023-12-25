import os
import cv2


def extract_all_files(source_dir, ext):
    files_list = []
    for (root,dirs,files) in os.walk(source_dir, topdown=True): 
        # print ('root',root) 
        # print ('dirs',dirs) 
        last_folder_name = os.path.basename(root)
        # print('last folder name:', last_folder_name)
        # print (files) 
        # break #exit for loop 
        # append files to list
        for file in files:
            if file.endswith(ext):  # or .jpg or .png
                files_list.append(root + '/'+file)
                
                
        # print ('--------------------------------') 
    return files_list

# Usage example
# source_directory = "../rgb_images/rugd1/" # uses png
# destination_directory = "../rgb_images/rugd/"
# source_directory = "../rgb_images/freiburg1/" # uses jpg
# destination_directory = "../rgb_images/freiburg/"
# source_directory = "../rgb_images/Rellis-3D/" #uses jpg
# destination_directory = "../rgb_images/rellis/"
# source_directory = "../rgb_images/ycor1/" #uses jpg
# destination_directory = "../rgb_images/ycor/"
source_directory = "../rgb_images/a2d21/" #uses png
destination_directory = "../rgb_images/a2d2/"

ext='.png'
result = extract_all_files(source_directory, ext)
# print(result) 
i=0
for image in result:
    # print(image)
    image2 = cv2.imread(image)
    # cv2.imshow('image',image2)
    # cv2.waitKey(100)
    print(i)
    i+=1
    file_name = os.path.basename(image) # used rugd, freiburg
    # file_name = os.path.basename(os.path.dirname(image)) +'.jpg'  # used ycor
    cv2.imwrite(destination_directory+file_name, image2)
    # print(file_name)
    # break

# ------------------------------

# # check to make sure file exists in both semantic and rgb folders

# dir1 = "../rgb_images/a2d2/"
# dir2 = "../semantic_images/a2d2/"

# # List all files in dir1
# files_in_dir1 = os.listdir(dir1)
# # print('Files in dir1:', files_in_dir1)


# file1_base = []
# for file in files_in_dir1:
#     name, extension = os.path.splitext(file)
#     file1_base.append(name)
# # print(file1_base)


# # List all files in dir2
# files_in_dir2 = os.listdir(dir2)
# # print('Files in dir2:', files_in_dir2)
# file2_base = []
# for file in files_in_dir2:
#     name, extension = os.path.splitext(file)
#     file2_base.append(name)
# # print(file2_base)

# # print size of file1_base
# print('len1: ', len(file1_base))
# # print size of file2_base
# print('len2: ', len(file2_base))

# # Check if all items in file1_base are in file2_base
# all_in_file2_base = all(item in file2_base for item in file1_base)

# print('All items in file1_base are in file2_base:', all_in_file2_base)

# ------------------------------
# removes the extra files

# # create list of items in file1_base that are not in file2_base
# not_in_file2_base = [item for item in file1_base if item not in file2_base]
# # print('Items in file1_base that are not in file2_base:', not_in_file2_base)
# print('len of items in file1_base that are not in file2_base:', len(not_in_file2_base))

# # Iterate over the list of filepaths & remove each file.
# # files in dir1 that are not in dir2
# for file in not_in_file2_base:
#     os.remove(dir1 + file + '.jpg')
#     print(file)

# print('len of items in file1_base that are not in file2_base:', len(not_in_file2_base))

# ------------------------------

# #remove with specific pattern 
# dir2 = "../rgb_images/a2d2/"
# # List all files in dir2
# files_in_dir2 = os.listdir(dir2)
# # print('Files in dir2:', files_in_dir2)
# file2_base = []
# for file in files_in_dir2:
#     name, extension = os.path.splitext(file)
#     file2_base.append(name)


# files_to_delete = []
# for file in file2_base:
#     # print(file[15:20])
#     # break
#     if file[15:20] == 'label':
#         # print(file)
#         # break
#         files_to_delete.append(file)
#         # print(dir2+file+'.png', dir2+file[:-4]+'Clipped.png')
#         # os.rename(dir2+file+'.png', dir2+file[:-4]+'Clipped.png')
# print('len of items to delete:', len(files_to_delete))

# # Iterate over the list of filepaths & remove each file.
# for file in files_to_delete:
#     os.remove(dir2 + file + '.png')
#     # print(file)


# ------------------------------

#rename properly 
# dir2 = "../semantic_images/freiburg/"
# # List all files in dir2
# files_in_dir2 = os.listdir(dir2)
# # print('Files in dir2:', files_in_dir2)
# file2_base = []
# for file in files_in_dir2:
#     name, extension = os.path.splitext(file)
#     file2_base.append(name)



# for file in file2_base:
#     if file[-4:] == 'mask':
#         print(file)
#         # print(dir2+file+'.png', dir2+file[:-4]+'Clipped.png')
#         os.rename(dir2+file+'.png', dir2+file[:-4]+'Clipped.png')

# dir2 = "../rgb_images/a2d2/"
# # List all files in dir2
# files_in_dir2 = os.listdir(dir2)
# # print('Files in dir2:', files_in_dir2)
# file2_base = []
# for file in files_in_dir2:
#     name, extension = os.path.splitext(file)
#     file2_base.append(name)



# for file in file2_base:
#     # print(file)
#     # print(file[15:21])
#     # print(file[0:15]+'label'+file[21:])
#     # break
#     if file[15:21] == 'camera':
#         # print(file)
#         # print(dir2+file+'.png', dir2+file[:-4]+'Clipped.png')
#         os.rename(dir2+file+'.png', dir2+file[0:15]+'label'+file[21:]+'.png')
# print('done')



# ----------------------------
# remove files with a specific extension 

# # Specify the directory and file extension
# dir_path = "../semantic_images/rellis/"
# file_extension = "*.Identifier"
# import glob
# # Use glob to match the file pattern
# files_to_delete = glob.glob(os.path.join(dir_path, file_extension))

# # Iterate over the list of filepaths & remove each file.
# for file in files_to_delete:
#     os.remove(file)
#     print(file)

# print("Files with extension", file_extension, "have been deleted from", dir_path)