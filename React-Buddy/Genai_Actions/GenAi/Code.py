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

def find_file(filename, directory):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

directory_path = "C:/Users/DGASERLAP177/Documents/GitHub/StocksGPT"
file_to_find = 'Login.tsx'

# Find the file
file_path = find_file(file_to_find, directory_path)

if file_path:
    # Read the file contents
    file_contents = read_file(file_path)
    print("File contents successfully read.")
else:
    print("File not found.")

# The variable file_contents now holds the contents of app.ts file

print(file_contents)
