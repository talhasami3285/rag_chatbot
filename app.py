from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from groq import Groq
import json
import logging
import uuid
app = Flask(__name__)
# Load environment variables from .env file
load_dotenv()
# Access API keys from environment variables
# groq_api_key = os.getenv("GROQ_API_KEY")
# serp_api_key = os.getenv("SERP_API_KEY")
serp_api_key="16bbf50d22c9bfa48733c5d94b72cb9a84f5aa23dc37f07bb45bc61549953bf9"
groq_api_key="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"
if not groq_api_key:
    raise ValueError("Groq API key not found. Ensure it is set in the .env file.")
if not serp_api_key:
    raise ValueError("SerpAPI key not found. Ensure it is set in the .env file.")
# Initialize the Groq client
client = Groq(api_key=groq_api_key)
# Ensure the 'chats' directory exists
if not os.path.exists('chats'):
    os.makedirs('chats')
def load_chat_history(user_id, chat_id):
    """Load chat history from a JSON file."""
    try:
        with open(f'chats/{user_id}/{chat_id}.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_chat_history(user_id, chat_id, history):
    """Save chat history to a JSON file."""
    user_folder = f'chats/{user_id}'
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    with open(f'{user_folder}/{chat_id}.json', 'w') as f:
        json.dump(history, f, indent=4)
# Function to perform Google search using SerpAPI
def google_search(query):
    params = {
        "q": query,
        "api_key": serp_api_key,
        "engine": "google"
    }
    response = requests.get("https://serpapi.com/search", params=params)
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
        image_response = requests.get("https://serpapi.com/search", params=image_params)
        image_results = image_response.json().get("images_results", [])
    if not video_results:
        # If inline videos are not available, use the video search engine
        video_params = {
            "q": query,
            "api_key": serp_api_key,
            "tbm": "vid"  # Video search
        }
        video_response = requests.get("https://serpapi.com/search", params=video_params)
        video_results = video_response.json().get("video_results", [])
    # Log the response for debugging
    logging.info(f"Google search response: {json.dumps(results, indent=2)}")
    return {
        "text_results": [
            {
                "title": result.get("title"),
                "snippet": result.get("snippet"),
                "link": result.get("link")
            } for result in text_results
        ],
        "image_results": [
            {
                "thumbnail": result.get("thumbnail"),
                "link": result.get("link")
            } for result in image_results
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
            } for question in related_questions
        ]
    }
@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    user_id = data.get('user_id')
    chat_id = data.get('chat_id')
    input_text = data.get('input_text')
    if not user_id or not chat_id or not input_text:
        return jsonify({"error": "user_id, chat_id, and input_text are required."}), 400
    # Load chat history for the given user ID and chat ID
    chat_history = load_chat_history(user_id, chat_id)
    # Prepare messages for Groq API to refine the search query
    refine_messages = []
    # Include previous chat history in the messages
    for entry in chat_history:
        refine_messages.append({
            "role": "user",
            "content": entry['prompt']
        })
        refine_messages.append({
            "role": "assistant",
            "content": entry['response']
        })
    # Add the new user input to the messages for refinement
    refine_messages.append({
        "role": "user",
        "content": f"Refine this prompt based on the previous conversation: {input_text}",
    })
    # Get refined prompt from Groq API
    refine_response = client.chat.completions.create(
        messages=refine_messages,
        model="llama3-8b-8192",
    )
    refined_prompt = refine_response.choices[0].message.content.strip()
    # Perform Google search with the refined prompt
    search_results = google_search(refined_prompt)
    # Extract relevant content from search results
    search_content = "\n".join([result.get('title', '') + "\n" + result.get('snippet', '') + "\n" + result.get('link', '') for result in search_results["text_results"]])
    # Prepare messages for Groq API to get a detailed response
    detailed_messages = []
    # Include previous chat history in the messages
    for entry in chat_history:
        detailed_messages.append({
            "role": "user",
            "content": entry['prompt']
        })
        detailed_messages.append({
            "role": "assistant",
            "content": entry['response']
        })
    # Add the refined prompt and search content to the messages
    detailed_messages.append({
        "role": "user",
        "content": f"Based on the refined prompt and the search results below, provide a detailed response:\n\nRefined Prompt: {refined_prompt}\n\nSearch Results:\n{search_content}",
    })
    # Get final detailed response from Groq API
    detailed_response = client.chat.completions.create(
        messages=detailed_messages,
        model="llama3-8b-8192",
    )
    llm_result = detailed_response.choices[0].message.content.strip()
    # Add user input and LLM result to history
    chat_history.append({'prompt': input_text, 'response': llm_result})
    # Save chat history back to the JSON file
    save_chat_history(user_id, chat_id, chat_history)
    # Construct response in the desired architecture
    response = {
        "user_id": user_id,
        "chat_id": chat_id,
        "prompt": input_text,
        "response": {
            "images": [
                {
                    "url": result.get('link', ''),
                    "source": result.get('thumbnail', '')
                } for result in search_results["image_results"]
            ],
            "videos": [
                {
                    "url": result.get('link', ''),
                    "source": result.get('thumbnail', '')
                } for result in search_results["video_results"]
            ],
            "related": [
                question.get('question') for question in search_results["related_questions"]
            ],
            "answer": {
                "value": llm_result,
                "sources": [
                    {
                        "heading": result.get('title', ''),
                        "Sub-Heading": result.get('snippet', ''),
                        "analytics": "Analytics info here",
                        "url": result.get('link', '')
                    } for result in search_results["text_results"]
                ]
            }
        }
    }
    return jsonify(response)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # app.run(host='0.0.0.0', debug=True)
    app.run()
