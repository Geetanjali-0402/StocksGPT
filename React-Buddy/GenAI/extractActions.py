import os
import json
import re
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

def extract_actions(file_path):
    if not file_path:
        print("File not found.")
        return None
    
    # Read the file contents
    file_contents = read_file(file_path)
    if not file_contents:
        print("Failed to read the file contents.")
        return None
    print("File contents successfully read.")

    if not file_path or not os.path.isfile(file_path):
        #print("File not found.")
        return "actions_path.json"
    
    prompt = f"""The input is a file path like {file_path} and output should be the actions that are being dispatched in this file 
    and display the action name and the exact path of the component which dispatches the action like Action: socialLogin, 
    Dispatched in: {file_path} Find all the actions that are being dispatched and used in the above code and write in key-value pairs
    where keys are the action names and values are its exact source path: {file_contents}"""
    
    response = chat.send_message(prompt)
    actions_path = response.text.strip()
    print(actions_path)

    return actions_path

def main():
    file_path = 'C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\pages\\Dashboard\\ConversationChat\\index.tsx'
    actions_path = extract_actions(file_path)
    
    if actions_path:
        # Convert the result to a dictionary
        actions_dict = {}
        action_lines = actions_path.split("\n")
        for line in action_lines:
            if line.startswith("Action:"):
                parts = line.split(", Dispatched in: ")
                if len(parts) == 2:
                    action_name = parts[0].replace("Action:", "").strip()
                    source_path = parts[1].strip()
                    actions_dict[action_name] = source_path
        
        # Save the dictionary to a JSON file
        output_file = 'actions_path.json'
        with open(output_file, 'w') as json_file:
            json.dump(actions_dict, json_file, indent=4)
        print(f"Actions path saved to {output_file}")

if __name__ == "__main__":
    main()
