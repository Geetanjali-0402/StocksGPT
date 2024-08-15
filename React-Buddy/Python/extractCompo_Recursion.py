from extractChildCompo import childComponents
from GetRoot_Components import getRoot
from readJsonFindComponent import extract_components_from_json
import os
import json
import sys

sys.setrecursionlimit(500)

seen_components=set()

def extractCompHierarchyRecursion(file_path, component_name, max_depth=1000, current_depth=0):
    """
    Recursively extracts the component hierarchy starting from the given component.
    """
    if current_depth > max_depth:
        print(f"Reached maximum recursion depth at component: {component_name}")
        return {}

    current_comp_json = {
        "name": component_name,
        "path_to_the_root_component": file_path,
        "hierarchy": []
    }

    if file_path:
        seen_components.add(component_name)
        child_path_json_file = childComponents(file_path)
        
        if not child_path_json_file:
            return current_comp_json  # Return if no child components are found

        child_hierarchy = extract_components_from_json(child_path_json_file)

        if not child_hierarchy:
            return current_comp_json  # Return if no child components are found

        for child in child_hierarchy:
            child_path = child["path"]
            child_name = child["name"]
            print(component_name+" "+child_name+" "+child_path)

            # Ensure child is not the same as the parent
            # if not(child_name in seen_components):
            if not(seen_components.__contains__(child_name)):
            
                # print("Child_name:", child_name, "seen_components:", seen_components)
                # print(seen_components.__contains__(child_name), " ", seen_components.__contains__("notpresentname"))
                # print(not(seen_components.__contains__(child_name)))
                seen_components.add(child_name)
                print("Entered this block")
                print(type(component_name))
                print(type(child_name), "\n\n")
                grandchild_hierarchy = extractCompHierarchyRecursion(
                    child_path, child_name, max_depth, current_depth + 1)
                child["hierarchy"] = grandchild_hierarchy
            else:
                child["hierarchy"] = []

        current_comp_json["hierarchy"] = child_hierarchy

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

    all_hierarchies = []

    for component in root_compo_data:
        file_path = component["path"]
        component_name = component["name"]

        if not os.path.exists(file_path):
            print(f"File '{file_path}' not found.")
            continue

        component_hierarchy = extractCompHierarchyRecursion(file_path, component_name)
        all_hierarchies.append(component_hierarchy)

    data = {"components": all_hierarchies}

    output_file_name = "hierarchy.json"
    with open(output_file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"All component hierarchies have been written to {output_file_name}")

if __name__ == "__main__":
    main()
