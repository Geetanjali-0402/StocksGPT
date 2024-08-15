import os
import json
from collections import defaultdict
from dotenv import load_dotenv
import google.generativeai as genai
from getComponents import processPathsFromJson, read_file

# Load environment variables
load_dotenv()

# Configure the Google Generative AI model
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key is None:
    raise ValueError("No GOOGLE_API_KEY found. Please set the environment variable.")

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config={"temperature": 0.0})
chat = model.start_chat(enable_automatic_function_calling=True)

def extract_events(file_path):
    if not file_path or not os.path.isfile(file_path):
        print("File not found.")
        return None
    
    # Read the file contents
    file_contents = read_file(file_path)
    if not file_contents:
        print("Failed to read the file contents.")
        return None
    print("File contents successfully read.")
    
    prompt = f"""The input is a file path like '{file_path}' 
    and the output should be the events found in this file. Display the event names which are in use, the name of the component related
    to the event, the function handling the event, actions dispatched by the event, and who triggers the event. 
    Format the output in key-value pairs where keys are the event names and values are dictionaries containing the component name,
    function name, dispatched actions, and trigger source: {file_contents}"""
    
    response = chat.send_message(prompt)
    events_details = response.text.strip()
    print(events_details)

    # Parse the response to create the events dictionary
    events_dict = {}
    event_lines = events_details.split("\n")
    for line in event_lines:
        if line.startswith("Event:"):
            parts = line.split(", ")
            event_name = parts[0].replace("Event: ", "").strip()
            component_name = parts[1].replace("Component: ", "").strip()
            function_name = parts[2].replace("Function: ", "").strip()
            dispatched_actions = parts[3].replace("Dispatched Actions: ", "").strip()
            trigger_source = parts[4].replace("Triggered by: ", "").strip()
            
            events_dict[event_name] = {
                "Component": component_name,
                "Function": function_name,
                "Dispatched Actions": dispatched_actions,
                "Triggered by": trigger_source
            }

    return events_dict

def main():
    file_path = 'C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\pages\\Authentication\\Login.tsx'
    events_dict = extract_events(file_path)
    
    if events_dict:
        # Save the dictionary to a JSON file
        output_file = 'events_details.json'
        with open(output_file, 'w') as json_file:
            json.dump(events_dict, json_file, indent=4)
        print(f"Events details saved to {output_file}")
    else:
        print("No events found or failed to extract events.")

if __name__ == "__main__":
    main()
