from extractChildCompo import childComponents
from GetRoot_Components import getRoot
from readJsonFindComponent import extract_components_from_json
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from getComponents import processPathsFromJson, find_file, read_file

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key is None:
    raise ValueError("No GOOGLE_API_KEY found. Please set the environment variable.")

# Configure the generative AI model
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name='gemini-1.0-pro')
chat = model.start_chat(enable_automatic_function_calling=True)


def extractCompHierarchyRecursion(file_path, component_name):
    """
    Recursively extracts the component hierarchy starting from the given component.
    """
    current_comp_json = {
        "name": component_name,
        "path_to_the_root_component": file_path,
        "hierarchy": []
    }

    if file_path is not None:
        child_path_json = childComponents(file_path)
        child_hierarchy = extract_components_from_json(child_path_json)

        current_comp_json["hierarchy"] = child_hierarchy

        if child_hierarchy:
            for child in child_hierarchy:
                child_path = child["path"]
                child_name = child["name"]
                grandchild_path_json = extractCompHierarchyRecursion(child_path, child_name)
                grandchild_hierarchy = extract_components_from_json(grandchild_path_json)
                child["hierarchy"] = grandchild_hierarchy
    
    return current_comp_json


def main():
    output_file_path = getRoot()
    if output_file_path:
        print(f"Root components have been successfully extracted and stored in {output_file_path}")
    else:
        print("Failed to extract root components.")
        return

    root_compo_data = extract_components_from_json(output_file_path)

    if not root_compo_data:
        print("No valid components found in the root components JSON.")
        return

    # List to hold all component hierarchies
    all_hierarchies = []

    for component in root_compo_data:
        file_path = component["path"]
        component_name = component["name"]

        # Ensure file_path is valid
        if not os.path.exists(file_path):
            print(f"File '{file_path}' not found.")
            continue

        # Process the component hierarchy recursively
        component_hierarchy = extractCompHierarchyRecursion(file_path, component_name)
        all_hierarchies.append(component_hierarchy)

    # Create the dictionary with the "components" key
    data = {"components": all_hierarchies}

    # Specify the output file name
    output_file_name = "hierarchy.json"

    # Write the data to a JSON file with pretty-printing
    with open(output_file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"All component hierarchies have been written to {output_file_name}")


if __name__ == "__main__":
    main()
