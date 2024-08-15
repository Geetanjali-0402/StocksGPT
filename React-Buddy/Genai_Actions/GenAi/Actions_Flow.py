


import os
import re

# Create a regex pattern to match action type constants (uppercase words with underscores)
pattern = re.compile(r'\b[A-Z_]+\b')

# Define the file paths with double backslashes
file_paths = [
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\forgetpwd\\actions.ts',
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\loginNode\\actions.ts',
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\register\\actions.ts',
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\layout\\actions.ts',
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\profile\\actions.ts',
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\settings\\actions.ts',
    r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\stockChats\\actions.ts'
]

# Function to find and print the action types in the files
def find_action_types(file_paths, pattern):
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            matches = pattern.findall(content)
            if matches:
                print(f"Matches in {file_path}:")
                for match in matches:
                    print(f"  {match}")

# Call the function
find_action_types(file_paths, pattern)


import re

# Input text
text = """
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\forgetpwd\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  FORGET_PASSWORD
  CHANGE_PASSWORD
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\loginNode\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  LOGIN_USER
  LOGOUT_USER
  SOCIAL_LOGIN
  GOOGLE_VERIFY
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\register\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  REGISTER_USER
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\layout\\actions.ts:
  CHANGE_TAB
  CHANGE_LAYOUT_MODE
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\profile\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  GET_PROFILE_DETAILS
  UPDATE_PROFILE_DETAILS
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\settings\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  GET_USER_SETTINGS
  UPDATE_USER_SETTINGS
  UPDATE_ALL_SETTINGS
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\stockChats\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  GET_STOCK_CHAT_TITLES
  ADD_NEW_CHAT
  DELETE_STOCK_CHAT
  GET_STOCK_CHAT_MESSAGES
  SEND_USER_MESSAGE
  RECEIVE_BOT_MESSAGE
  SET_SHOW_WELCOME_SCREEN_FLAG
  CHANGE_SELECTED_STOCK_CHAT
"""

# Regular expression to match action names (uppercase words with at least 2 characters)
pattern = r'\b[A-Z_]{2,}\b'

# Find all matches
matches = re.findall(pattern, text)

# Print the list of action names
print(matches)


import re
from collections import defaultdict

# Define the base path with a placeholder
base_path = r'C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\{}\\reducer.ts'

# List of specific subdirectory names
subdirs = [
    'auth\\forgetpwd',
    'auth\\loginNode',
    'auth\\register',
    'layout',
    'profile',
    'settings',
    'stockChats'
]

# Create a regex pattern to match lines with action types
pattern = re.compile(r'\b[A-Z_]+\b')

# Define the output text
output_text = """
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\forgetpwd\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  FORGET_PASSWORD
  CHANGE_PASSWORD
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\loginNode\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  LOGIN_USER
  LOGOUT_USER
  SOCIAL_LOGIN
  GOOGLE_VERIFY
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\auth\\register\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  REGISTER_USER
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\layout\\actions.ts:
  CHANGE_TAB
  CHANGE_LAYOUT_MODE
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\profile\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  GET_PROFILE_DETAILS
  UPDATE_PROFILE_DETAILS
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\settings\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  GET_USER_SETTINGS
  UPDATE_USER_SETTINGS
  UPDATE_ALL_SETTINGS
Matches in C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\stockChats\\actions.ts:
  API_RESPONSE_SUCCESS
  API_RESPONSE_ERROR
  GET_STOCK_CHAT_TITLES
  ADD_NEW_CHAT
  DELETE_STOCK_CHAT
  GET_STOCK_CHAT_MESSAGES
  SEND_USER_MESSAGE
  RECEIVE_BOT_MESSAGE
  SET_SHOW_WELCOME_SCREEN_FLAG
  CHANGE_SELECTED_STOCK_CHAT
"""

# Dictionary to store counts of action types for each file
action_counts = defaultdict(lambda: defaultdict(int))

# Split the output text into lines and process each line
lines = output_text.splitlines()
current_file = None

for line in lines:
    # Check if the line indicates a file path
    file_match = re.match(r'Matches in (C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\[\w\\]+\\actions\.ts):', line)
    if file_match:
        current_file = file_match.group(1).replace('actions.ts', 'reducer.ts')
    elif current_file:
        # Match action types in the line
        action_matches = pattern.findall(line)
        for action in action_matches:
            action_counts[current_file][action] += 1

# Print the results
for file_path, counts in action_counts.items():
    print(f"Counts in {file_path}:")
    for action_type, count in counts.items():
        print(f"  {action_type}: {count}")



# Navigate back to the parent directory
current_directory = "C:\\Users\\DGASERLAP177\\Documents\\GitHub\\StocksGPT\\src\\redux\\stockChats\\reducer.ts"
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

# Saga file path
saga_file = "saga.ts"

# Function to check if the keyword exists in the saga file
def keyword_in_saga(keyword, saga_file):
    with open(saga_file, 'r') as f:
        content = f.read()
        if keyword in content:
            return True
    return False


# Iterate over keywords and check if they exist in the saga file
for keyword in filtered_keywords:
    if keyword_in_saga(keyword, os.path.join(parent_directory, saga_file)):
        print(f"Keyword '{keyword}' found in saga.ts file")



