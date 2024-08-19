import sqlite3
import json
from datetime import datetime

from src.GenAI.FunctionCalling.models import GeminiModel as GM
from src.GenAI.FunctionCalling.models import data_retriever_util as dr
from src.GenAI.FunctionCalling.models import indicator_util as inu

# Function to create the SQLite database table if it doesn't exist
def create_table():
    # closing any open connection...

    conn = sqlite3.connect('src/Data/prompt_cache.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prompts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 original_prompt TEXT,
                 clean_prompt TEXT,
                 prompt_output TEXT,
                 timestamp TEXT,
                 frequency INTEGER)''')
    conn.commit()
    conn.close()

# Function to clean the prompt
def clean_prompt(prompt):
    # Add your cleaning operations here
    clean_prompt = prompt.strip().lower()  # Example: Removing leading/trailing spaces and converting to lowercase
    return clean_prompt

# Function to check if a prompt already exists in the cache
def prompt_exists(clean_prompt):
    # try:
    conn = sqlite3.connect('src/Data/prompt_cache.db')
    # except:
    #     create_table()
    #     conn = sqlite3.connect('src/Data/prompt_cache.db')

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM prompts WHERE clean_prompt=?", (clean_prompt,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# Function to add a prompt to the cache
def add_prompt(original_prompt, clean_prompt, prompt_output):
    # print(prompt_output)
    conn = sqlite3.connect('src/Data/prompt_cache.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO prompts (original_prompt, clean_prompt, prompt_output, timestamp, frequency) VALUES (?, ?, ?, ?, 1)",
              (original_prompt, clean_prompt, json.dumps(prompt_output), timestamp))
    conn.commit()
    conn.close()

# Function to fetch prompt output from the cache
def fetch_cached_output(clean_prompt):
    conn = sqlite3.connect('src/Data/prompt_cache.db')
    c = conn.cursor()
    c.execute("SELECT prompt_output, frequency FROM prompts WHERE clean_prompt=?", (clean_prompt,))
    result = c.fetchone()
    if result:
        output, frequency = result
        # Increment frequency
        new_frequency = frequency + 1
        c.execute("UPDATE prompts SET frequency=? WHERE clean_prompt=?", (new_frequency, clean_prompt))
        conn.commit()
        conn.close()
        return json.loads(output)
    else:
        conn.close()
        return None
    
# [{'role': 'user', 'parts': ['User request:  "sbi stock price for 2020 and show 20 days moving average"\n    just give me comma separated python list of technical incators mentioned in the chat till now\n    Output format: "indicators=[...]" ']},
#  {'role': 'user', 'parts': ['User request:  "indicators=[]"\n    We already have dataframe called OHLC_df  which contains \'open\', \'high\', \'low\', \'close\' and \'volume\' data.  Please can you provide the lines of Python code which need to be applied to this \'OHLC_df\' in order to produce the requisite indicators requested by User.\n    Dont plot the graph please. and give the code as string only. And add the new indicator to the OHLC_df. dont use talib module']}]

def generate_prompt_output(prompt, chatHistory):
    # Change the model here to any model you want. Make sure it returns the response in the same format!
    formated_chatHistory=dr.getHistory(chatHistory, "Gemini_Pro_PromptCall_with_chatHistory")
    response = GM.Gemini_Pro_PromptCall_with_chatHistory(formated_chatHistory, prompt)
    # if prompt is None:
    #     prompt = {}
    return response

# Function to handle a new prompt
def handle_new_prompt(original_prompt, chatHistory, string_representation_of_chatHistory):
    create_table()
    clean_prompt_text = clean_prompt(string_representation_of_chatHistory)
    requiredData = None
    if not prompt_exists(clean_prompt_text):
        generated_output = generate_prompt_output(original_prompt, chatHistory)
        add_prompt(original_prompt, clean_prompt_text, generated_output)

        # Perform the database calculations
        requiredData = dr.getRequiredData(generated_output)
    else:
        # print("------------Prompt cached")

        # Prompt already exists, fetch and return the output from the cache
        generated_output = fetch_cached_output(clean_prompt_text)
        requiredData = dr.getRequiredData(generated_output)

    if requiredData is not None:
        # plotlyJson = dr.plotGraph(requiredData["dataFrame"], requiredData["stockName"])
        plotlyJsonDaily = inu.indicatorGenerator(original_prompt, chatHistory, requiredData["dataFrame"], requiredData["stockName"])
        plotlyJsonWeekly = dr.compute_resample_data(requiredData["dataFrame"], requiredData["stockName"], "W")
        plotlyJsonMonthly = dr.compute_resample_data(requiredData["dataFrame"], requiredData["stockName"], "M")

        return {
            'message_text': json.dumps({ 
                "startDate": requiredData["startDate"],
                "endDate": requiredData["endDate"],
                "stockName": requiredData["stockName"],
                "functionCalled": requiredData["functionCalled"],
                "model": requiredData["model"],
                "response": requiredData["response"]
            }),
            # 'text': f"Daily Candle Chart for {requiredData["stockName"]} from {requiredData["startDate"]} to {requiredData["endDate"]}",
            'plotlyJson' : json.dumps({
                'daily': plotlyJsonDaily,
                'weekly': plotlyJsonWeekly,
                'monthly': plotlyJsonMonthly
            })
        }
    return {
        'message_text': json.dumps({}),
        'plotlyJson' : json.dumps({})
    }

# Function to handle the chat title
def handle_chat_title(original_prompt):
    create_table()
    clean_prompt_text = clean_prompt(original_prompt)
    requiredData = None
    if not prompt_exists(clean_prompt_text):
        generated_chatTitle = GM.Gemini_Pro_PromptCall_for_chat_title(original_prompt)
        add_prompt(original_prompt, clean_prompt_text, generated_chatTitle)

        # Perform the database calculations
        requiredData = generated_chatTitle
    else:
        # print("------------Title cached")
        # Prompt already exists, fetch and return the output from the cache
        generated_chatTitle = fetch_cached_output(clean_prompt_text)
        requiredData = generated_chatTitle

    if requiredData is not None:
        return { 'chatTitle':  requiredData["chatTitle"] }
    return { 'chatTitle':  "No-Title" }

# Main function to test the implementation
# if __name__ == "__main__":
# create_table()
#     # Example usage
#     prompt = "Example prompt"
#     output = handle_new_prompt(prompt)
#     print("Output for prompt:", output)
