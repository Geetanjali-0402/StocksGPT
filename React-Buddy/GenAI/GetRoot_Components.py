from getComponents import processPathsFromJson,find_file,read_file

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

model = genai.GenerativeModel(model_name='gemini-1.0-pro')
chat = model.start_chat(enable_automatic_function_calling=True)
google_api_key = os.getenv('GOOGLE_API_KEY')

if google_api_key is None:
    raise ValueError("No GOOGLE_API_KEY found. Please set the environment variable.")

genai.configure(api_key=google_api_key)

def getRoot():
    #getting the root component path
    directory_path = "C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\pages\\Authentication"
    file_to_find = 'Login.tsx'
    file_path = find_file(file_to_find, directory_path)

    if file_path:
        # Read the file contents
        file_contents = read_file(file_path)
        print("File contents successfully read.")
    else:
        print("File not found.")

    #getting the components
    response = chat.send_message('Find all the Components that are being used in the above code and write in key value pairs where keys are the component names and values are its exact source path:'+file_contents)
    routes_path=response.text
    print(routes_path)

    # Process the input data to create a list of components
    components = []
    for line in routes_path.strip().split('\n'):
        name, path = line.split(': ')
        components.append({"name": name.strip('- '), "path": path})

    # Create the dictionary with the "components" key
    data = {"components": components}

    # Specify the output file name
    file_name = "components.json"

    # Write the data to a JSON file with pretty-printing
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data has been written to {file_name}")

    FolderPathPython = "C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\pages\\Authentication"
    jsonFilePath = "components.json"  # Assuming this file contains the JSON array of paths
    resolved_paths = processPathsFromJson(jsonFilePath, FolderPathPython)
    data = {"components": resolved_paths}

    # Specify the output file name
    output_file_name = "components_path.json"
    # Write the data to a JSON file with pretty-printing
    with open(output_file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data has been written to {output_file_name}")
    return output_file_name