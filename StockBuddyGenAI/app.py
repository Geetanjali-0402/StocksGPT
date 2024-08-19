import time
from flask import Flask, request, jsonify
from src.Data.data_utils import NSE_table_updater as ntu, prompt_cache_manager as pcm
import threading

from src.GenAI.FunctionCalling.models import GeminiModel as GM
from src.GenAI.FunctionCalling.models import data_retriever_util as dr


app = Flask(__name__)


@app.route('/api/generateFromChatHistory', methods=['POST'])
def generateFromChatHistory():
    data = request.get_json()  # Get the request data, expected to contain the prompt
    chatHistory = data.get('chatHistory', '')
    # print("chat history is:", chatHistory)

    if not chatHistory:
        return jsonify({'error': 'No History provided'}), 400

    # try:
    # generated_text = generate_text(prompt)
    rectified_chatHistory, last_prompt = dr.rectify_chatHistory_from_Middleware(chatHistory)
    # last_prompt = "sbi stock data from jan to feb 2020"
    string_representation_of_chatHistory = str(chatHistory)
    response = pcm.handle_new_prompt(last_prompt, rectified_chatHistory, string_representation_of_chatHistory)
    # print("Chat History>>", rectified_chatHistory, "prompt>>", last_prompt)
    # print("response>>",response)
    return jsonify(response if response is not None else {})
        
    # except Exception as e:
    #     print("Error in generateFromChatHistory is: ", e)
    #     return jsonify({'error': str(e)}), 500
    
@app.route('/api/generateFromSinglePrompt', methods=['POST'])
def generateFromSinglePrompt():
    data = request.get_json()  # Get the request data, expected to contain the prompt
    userPrompt = data.get('userPrompt', '')
    print("user prompt is:", userPrompt)

    if not userPrompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # userPrompt = "can you give me past 5 years of aspinwall stock?"; # rewriting and hard coding the prompt
        userPrompt = "april to feb sbi stock 2020"
        response = pcm.handle_new_prompt(userPrompt, [], "")

        # print(response)
        return jsonify(response if response is not None else {})
    except Exception as e:
        print("Error: ", e)
        return jsonify({'error': str(e)}), 500


@app.route('/api/generateChatTitle', methods=['POST'])
def generateChatTitle():
    data = request.get_json()  # Get the request data, expected to contain the prompt
    userPrompt = data.get('userPrompt', '')
    print("user prompt is:", userPrompt)

    if not userPrompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response_title = pcm.handle_chat_title(userPrompt)
        return jsonify(response_title)
    except Exception as e:
        print("Error in chat title function is ", e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    background_thread = threading.Thread(target=ntu.background_task)
    background_thread.daemon = True  # Daemonize the thread so it automatically stops when the main thread stops
    background_thread.start()
    # time.sleep(1000)
    app.run(use_reloader=False)  # Starts the Flask application