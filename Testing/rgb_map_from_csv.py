import csv
import colorsys
import json 


def convert_to_rgb(value, min_value, max_value):
    # Calculate the range of values
    value_range = max_value - min_value

    # Calculate the position of the value within the range
    position = (value - min_value) / value_range

    # Convert the position to a hue in the HSV color space
    hue = position

    # Use full saturation and value
    saturation = 1.0
    value = 1.0
    
    
    # Convert the HSV color to RGB
    red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)

    # Convert the RGB values from the range [0, 1] to [0, 255]
    red = int(red * 255)
    green = int(green * 255)
    blue = int(blue * 255)
    return red, green, blue

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present
        rows = list(reader)  # Store the rows in a list
        max_value = 0 # Some small number
        min_value = 100000 # Some large number
        
        for row in rows:
            value = int(row[2])  # Assuming the value is in the third column
            if value > max_value:
                max_value = value
            if value < min_value:
                min_value = value
        
        # print('max val: ', max_value, ' min val: ', min_value)
        
        results = []  # Create a list to store the results
        for row in rows:
            value = int(row[2])  # Assuming the value is in the third column
            rgb = convert_to_rgb(value, min_value, max_value+1)  
            class_name = row[0]
            class_value = row[2]
            results.append((class_name, rgb, class_value))  # Append the class_name and rgb to the results list
            # print(class_name, rgb)
        
        # print('Done')
    return results

def save_to_json(results, json_file_path):
    # Define the Processing_Properties
    data = {
        "Processing_Properties": {
            "parameters": {
                "ATLAS_version": "2.0.4",
                "img_extension": ".png",
                "min_polygon_size": 100
            }
        },
        "Color_Information": {}
    }

    # Add the Color_Information
    for class_name, rgb, class_value in results:
        red, green, blue = rgb
        data["Color_Information"][class_name] = {
            "red_value": red,
            "green_value": green,
            "blue_value": blue,
            # add class value
            "class_value": class_value
        }

    # Write the data to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Usage example
csv_file_path = 'Mappings_RGB/unify_dataset.csv'
json_file_path = 'Mappings_RGB/unify_dataset_rgb.json'
result = read_csv_file(csv_file_path)

# for i in result:
#     print(i)

save_to_json(result, json_file_path)

print('Done')