from getComponents import processPathsFromJson,find_file,read_file

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

model = genai.GenerativeModel(model_name='gemini-1.0-pro',generation_config={"temperature": 0.0})
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

    prompt = f"""The input is the root file path like 'C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\pages\\Authentication' 
    and output should be the components that are being used inside this file and display their name and the exact path like
    Name: NonAuthLayoutWrapper, Path: C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\components\\NonAuthLayoutWrapper.tsx
    Find all the Components that are being used in the above code without taking into account those components which are under node
    modules folder and write in key value pairs where keys are the component names and values are its exact source path: {file_contents}"""
    
    response = chat.send_message(prompt)
    routes_path = response.text
    print(routes_path)

    # Process the input data to create a list of components
    components = []
    for line in routes_path.strip().split('\n'):
        if ', ' in line:
            name_part, path_part = line.split(', ', 1)
            name = name_part.split(': ')[1]
            path = path_part.split(': ')[1]
            components.append({"name": name.strip(), "path": path.strip()})

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