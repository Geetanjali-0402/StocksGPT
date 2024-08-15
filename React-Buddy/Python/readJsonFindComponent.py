import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Assuming you have set up the GOOGLE_API_KEY environment variable
google_api_key = os.getenv('GOOGLE_API_KEY')

if google_api_key is None:
    raise ValueError("No GOOGLE_API_KEY found. Please set the environment variable.")

genai.configure(api_key=google_api_key)

def find_file(filename, directory):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    except IOError as e:
        print(f"An error occurred while trying to read the file at {file_path}: {e}")
        return None

def process_file_with_generative_ai(file_path, chat):
    # Read the file contents
    file_contents = read_file_contents(file_path)
    if file_contents is None:
        print(f"File at '{file_path}' could not be read.")
        return
    
    # Send prompt to Generative AI for components
    response = chat.send_message(f'Find all the Components that are being used in {file_path} and write in key value pairs where keys are the component names and values are its exact source path:\n{file_contents}')
    routes_path = response.text.strip()
    
    # Process the response to extract components
    components = []
    for line in routes_path.split('\n'):
        if ': ' in line:
            name, path = line.split(': ', 1)
            components.append({"name": name.strip(), "path": path.strip()})
    
    return components

def extract_components_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            components = data.get('components', [])  # Get the 'components' array from JSON
            
            # Create a list of dictionaries with name and path of each component
            components_list = [{"name": component['Component name'], "path": component['path']} for component in components]
            return components_list
    except FileNotFoundError:
        print(f"The JSON file at {json_file_path} was not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {json_file_path}: {e}")
        return []
    except IOError as e:
        print(f"An error occurred while trying to read the JSON file at {json_file_path}: {e}")
        return []

def main():
    json_file_path = "C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\Python\\components_path.json"  # Replace with your JSON file containing paths

    # Read paths from JSON file
    paths_data = extract_components_from_json(json_file_path)
    if paths_data:
        for component in paths_data:
            print(f"Component Name: {component['name']}, Path: {component['path']}")
    

    print("\n\n")

    # Initialize Generative AI chat session
    model = genai.GenerativeModel(model_name='gemini-1.0-pro')
    chat = model.start_chat(enable_automatic_function_calling=True)

    # Process each file path from JSON data
    for file_path in paths_data:
        # Ensure file_path is valid
        if not os.path.exists(file_path):
            print(f"File '{file_path}' not found.")
            continue
        
        # Process file with Generative AI
        components = process_file_with_generative_ai(file_path, chat)

        # Create the dictionary with the "components" key
        data = {"components": components}

        # Specify the output file name based on the file path
        file_name = os.path.basename(file_path) + "_components.json"

        # Write the data to a JSON file with pretty-printing
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Data for file '{file_path}' has been written to {file_name}")

if __name__ == "__main__":
    main()
