import os

def load_images_with_name(image_name, folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter files with the given image name
    matching_files = [file for file in files if file.startswith(image_name)]

    # Return the matching file paths
    return [os.path.join(folder_path, file) for file in matching_files]

# Example usage
#image_name = "img59.jpg"
#folder_path = "uploads"
#image_paths = load_images_with_name(image_name, folder_path)

# Print the paths of the matching images
#for path in image_paths:
#    print(path)
