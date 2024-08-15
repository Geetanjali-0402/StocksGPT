import os
import json

def find_file(filename, directory):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_file(filepath):
    if not os.path.isfile(filepath):
        #print(f"File not found: {filepath}")
        return None
    with open(filepath, 'r') as file:
        return file.read()


def fileNavigator(FolderPathPython, JsRelativePath):
    # Extracting the number of upward folders and the relative folder path from JsRelativePath
    split_path = JsRelativePath.split('/')
    NoOfUpFolders = sum(1 for part in split_path if part == '..')
    JsRelativeFolderPath = '/'.join(part for part in split_path if part not in ['..', '.'])
    
    # Converting JsRelativeFolderPath to Python relative folder path
    PyRelativeFolderPath = JsRelativeFolderPath.replace('/', '\\')
    
    # Splitting FolderPathPython into components
    folder_components = FolderPathPython.split('\\')
    
    # Trimming the folder path based on NoOfUpFolders
    if NoOfUpFolders > 0:
        TrimmedFolderPathPython = '\\'.join(folder_components[:-NoOfUpFolders])
    else:
        TrimmedFolderPathPython = FolderPathPython
    
    # Constructing the new file path
    NewFilePath = os.path.join(TrimmedFolderPathPython, PyRelativeFolderPath)
    
    return NewFilePath

# Function to read JS relative paths from a JSON file and process each
def processPathsFromJson(jsonFilePath, FolderPathPython):
    # Read the JSON file
    with open(jsonFilePath, 'r') as file:
        jsPaths = json.load(file)
    
    result = []

    # Process each component's JS relative path and print the new file path
    for component in jsPaths["components"]:
        name = component["name"]
        JsRelativePath = component["path"].strip('`')
        new_file_path = fileNavigator(FolderPathPython, JsRelativePath)
        new_file_path_with_extension = new_file_path 
        result.append({"Component name": name, "path": new_file_path_with_extension})
        print(f"Component Name: {name} -> New file path: {new_file_path_with_extension}")
    
    return result
