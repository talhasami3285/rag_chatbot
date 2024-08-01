
# from api import apikey
from flask import Flask, request, jsonify,Response
import pandas as pd
from csv import writer
from langchain.embeddings import OpenAIEmbeddings
import pandas as pd
import requests
from langchain.vectorstores import Chroma
import os
import re
# from openai import OpenAI
import json
import jsonpickle
# from PIL import Image
import tiktoken
from groq import Groq


# To get the tokeniser corresponding to a specific model in the OpenAI API:

from flask_cors import CORS, cross_origin
# apikeys = apikey

app = Flask(__name__)

cors = CORS(app)
# client = OpenAI(api_key=apikeys)



serp_api_key="0f5899b4ba2f0c30838bef2124fbdbfd6b72653522a1f2436aaafb3276a8e01b"
groq_api_key="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"

client = Groq(api_key=groq_api_key)
if not groq_api_key:
    raise ValueError("Groq API key not found. Ensure it is set in the .env file.")
if not serp_api_key:
    raise ValueError("SerpAPI key not found. Ensure it is set in the .env file.")





def folder_check(folder_path):
    """Create a folder if it does not already exist."""
    if not os.path.exists("chats//"+folder_path):
        os.makedirs("chats//"+folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

####################################### GET ALL THE LISTING
def google_search(query):
    params = {
        "q": query,
        "api_key": serp_api_key,
        "engine": "google"
    }
    print("Searching Google : ",query)
    response = requests.get("https:/serpapi.com/search", params=params)
    results = response.json()
    text_results = results.get("organic_results", [])
    image_results = results.get("inline_images", [])
    video_results = results.get("inline_videos", [])
    related_questions = results.get("related_questions", [])

    if not image_results:
        # If inline images are not available, use the image search engine
        image_params = {
            "q": query,
            "api_key": serp_api_key,
            "tbm": "isch"  # Image search
        }
        image_response = requests.get("https:/serpapi.com/search", params=image_params)
        image_results = image_response.json().get("images_results", [])

    if not video_results:
        # If inline videos are not available, use the video search engine
        video_params = {
            "q": query,
            "api_key": serp_api_key,
            "tbm": "vid"  # Video search
        }
        video_response = requests.get("https:/serpapi.com/search", params=video_params)
        video_results = video_response.json().get("video_results", [])

    # Log the response for debugging
    # logging.info(f"Google search response: {json.dumps(results, indent=2)}")

    return {
        "text_results": [
            {
                "title": result.get("title"),
                "snippet": result.get("snippet"),
                "link": result.get("link")
            } for result in text_results[:5]
        ],
        "image_results": [
            {
                "thumbnail": result.get("thumbnail"),
                "link": result.get("link")
            } for result in image_results[:5]
        ],
        "video_results": [
            {
                "title": result.get("title"),
                "link": result.get("link"),
                "thumbnail": result.get("thumbnail")
            } for result in video_results[:5]  # Only first 5 videos
        ],
        "related_questions": [
            {
                "question": question.get("question"),
                "snippet": question.get("snippet"),
                "link": question.get("link")
            } for question in related_questions[:5]
        ]
    }
#################################################### COUNT TOKEN


def extract_between_triple_backticks(text):
    """
    Extracts the substring from text that is between triple backticks (```).

    Parameters:
    text (str): The input string from which to extract the substring.

    Returns:
    str: The extracted substring, or an empty string if triple backticks are not found.
    """
    match = re.search(r'```(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""
def extract_between_backticks(text):
    """
    Extracts the substring from text that is between backticks (`).

    Parameters:
    text (str): The input string from which to extract the substring.

    Returns:
    str: The extracted substring, or an empty string if backticks are not found.
    """
    try:
        start_index = text.index('`') + 1
        end_index = text.index('`', start_index)
        return text[start_index:end_index]
    except ValueError:
        return "" 
############## GPT PROMPT ####################
def gpt(inp,listing):
    systems = {"role": "system", "content": """ 
              You're an real state AI agent that is connected with google serp API. whenever you need data from google return 
            ```
               <your Google search>.
            ```
            
            you'll get the data in system chat.
               IMPORTANT: Dont do google search unnecessary only do when its needed.
               IMPORTANT: ONLY RETURN GOOGLE SEARCH QUERY WHEN YOU NEED DONT REPLY ANOTHER STUFF.
               IMPORTANT: Prefare GOOGLE SEARCH WHENEVER USE ASK ABOUT ANY PROPERTY use three backlist for search
              """}
    new_inp = inp
    new_inp.insert(0,systems)
    if listing != "":
        system2 = {"role":"system","content":f"The properties in JSON"+str(listing['text_results'])+" Now send this to User with some Detail and URLs make it proper message"}
        new_inp.insert(1,system2)
    for item in new_inp:
        if 'search_results' in item:
            del item['search_results']
    
    completion = client.chat.completions.create(
    model="llama3-70b-8192", 
    messages=new_inp
    )
    return completion

############    GET CHATS BY USER ID ##################
def get_chats(id):
    path = id
    isexist = os.path.exists(path)
    if isexist:
        data = pd.read_json(path)
        # print(data)
        chats = data.chat
        return  list(chats)
    else:
        return "No Chat found on this User ID."



def url_fetch(text):    
    url_pattern = r'https?:/[^/s)/]]+'

    # Finding all URLs in the string
    urls = re.findall(url_pattern, text)

    # Print the list of URLs
    # for url in urls:
    #     print(url)
    return urls




############### APPEND NEW CHAT TO USER ID JSON FILE #################
def write_chat(new_data, id):
    with open(id,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["chat"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)



    



##################################
def handle_prompt(prompt,path):
        write_chat({"role":"user","content":prompt,"search_results":[]},path)
        # print()
        chats = get_chats(path)
        chats = chats[-6:]
        print(chats)
        # print("GETCHATS /n/n ",chats)
        send = gpt(chats,"")
        
        reply = send.choices[0].message.content
        print("reply   ...............:  ",reply)
        if "`" in str(reply) :
            if "```" in str(reply):
                print('/n/nBacklist Found/n/n: ',reply)
                reply = extract_between_triple_backticks(str(reply))
            else:
                reply = extract_between_backticks(str(reply))


        
            # extract_between_backticks
            reply = reply.replace("`","")

            listing = ""

            listing = google_search(str(reply))

            
            if listing !=  'None':
                print("we hare at 1")
                # print("We got listing : ",listing)
                # write_chat({"role":"system","content":f"The properties in JSON"+str(listing['text_results'])+" Now send this to User with some Detail and URLs make it proper message"},path)
                chats = get_chats(path)
                chats = chats[-6:]
                send = gpt(chats,listing)
                # print("Get Google response from GPT: ",send)
                reply = send.choices[0].message.content
                print("Get Google response from GPT: ",reply)
                write_chat({"role":"assistant","content":reply,"search_results":listing},path)   
                # return Response(reply, mimetype='text/html')
                reply = reply.replace("<b>","<br><b>")
                return {"message":reply,"status":"OK","search_result":listing}
                # return 'ok'
   

        else:
            print("reply    ",reply)
            write_chat({"role":"assistant","content":reply},path)
            return {"message":reply,"status":"OK","search_result":[]}
            # return Response(reply, mimetype='text/html')
            # return 'ok'

    
################################ CHECK IF USER IS ALREADY EXIST IF NOT CREATE ONE ELSE RETURN GPT REPLY ##################
@app.route('/chat', methods=['POST'])
@cross_origin()
def check_user():
    # image_url = 'https:/www.estraha.com/assets/uploads/property_image'
    ids = request.json['user_id']
    prompt = request.json['prompt']
    chat_id = request.json['chat_id']
    folder_check(ids)
    # print("asd")
    path = str(os.getcwd())+'//chats//'+ids+"//"+chat_id+'.json'
    print(path)
    # path = str(os.getcwd())+'//'+"5467484.json"
    isexist = os.path.exists(path)
    if isexist:
        # try:
        print(path," found!")
        a = handle_prompt(prompt,path)
        return 'ok' 


    else:
        print(path," Not found!")
        dictionary = {
        "user_id":ids,
        "chat":[]


        }
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        
        # Writing to sample.json
        with open(path, "w") as outfile:
            outfile.write(json_object)
        reply = check_user()
        return reply
    



####################   NEW ENPOINT GET CHATS ##############################
@app.route('/chat', methods=['GET'])
@cross_origin()
def get_chatss():
    ids = request.args.get('user_id')
    chat_id = request.args.get('chat_id')
    path = str(os.getcwd())+'//chats//'+ids+"//"+chat_id+'.json'
    print(path)
    return jsonpickle.encode(get_chats(path))


@app.route('/chat', methods=['PUT'])
@cross_origin()
def put_chats():
    ids = request.json['user_id']
    prompt = request.json['prompt']
    chat_id = request.json['chat_id']
    path = str(os.getcwd())+'//chats//'+ids+"//"+chat_id+'.json'
    print(path)
    a = handle_prompt(prompt,path)
    return a




######################################################### clear chats
@app.route('/delete_chats', methods=['POST'])
@cross_origin()
def clear_chatss():
    ids = request.json['user_id']

    try:
        path =os.remove(str(os.getcwd())+'/chats/'+ids+'.json')
     
        return {"status":"OK","message":"success"}
 
    except :
        return { "status":"error","message":"Something went wrong,chat doesn't exist" }




################################ GET ALL USER'S IDs
@app.route('/conversations', methods=['GET'])
@cross_origin()
def conversations():
    """
    Fetches all JSON files in the specified directory and reads their content.

    Parameters:
    directory_path (str): The path of the directory to search for JSON files.

    Returns:
    dict: A dictionary where keys are file names and values are the content of the JSON files.
    """


    user_id = request.args.get('user_id')
    path = "chats/"+user_id
    json_files_with_first_message = []
    try:
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                file_path = os.path.join(path, filename)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'chat' in data and isinstance(data['chat'], list) and len(data['chat']) > 0:
                        first_message = data['chat'][0].get('content', 'No content')
                        json_files_with_first_message.append({
                            "file_name": filename.replace(".json",""),
                            "first_message": first_message
                        })
    except Exception as e:
        print(f"An error occurred: {e}")

    return json_files_with_first_message

if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0',threaded=True)
    
    
