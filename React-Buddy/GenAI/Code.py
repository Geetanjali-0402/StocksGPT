import google.generativeai as genai
from dotenv import load_dotenv

import json
import os
import pathlib
import textwrap
import time




# Load environment variables from .env file
load_dotenv()

# Access the GOOGLE_API_KEY environment variable
google_api_key = os.getenv('GOOGLE_API_KEY')

# Configure the genai API
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name='gemini-1.0-pro')
chat = model.start_chat(enable_automatic_function_calling=True)

import os

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
