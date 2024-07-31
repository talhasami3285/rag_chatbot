# import streamlit as st
# import requests

# # URL of your Flask API
# FLASK_API_URL = "http://127.0.0.1:5000/api/query"

# # Streamlit app setup
# st.title("Graq.ai and Google Search Integration")

# # Input fields
# user_id = st.text_input("Enter your User ID")
# input_text = st.text_input("Search the topic you want")

# # Button to send request to Flask API
# if st.button("Submit"):
#     if user_id and input_text:
#         # Prepare the request payload
#         payload = {
#             "user_id": user_id,
#             "input_text": input_text
#         }
        
#         # Send POST request to Flask API
#         try:
#             response = requests.post(FLASK_API_URL, json=payload)
#             response.raise_for_status()
#             data = response.json()
            
#             # Display the Google search results
#             st.write("Google Search Results:")
#             for result in data.get("google_results", []):
#                 st.write(f"**Title:** {result.get('title', 'No title')}")
#                 st.write(f"**Snippet:** {result.get('snippet', 'No snippet')}")
#                 st.write("---")
            
#             # Display the LLM response
#             st.write("Graq Response:")
#             st.write(data.get("llm_result", "No result available"))
            
#             # Display the chat history
#             st.write("Chat History:")
#             for entry in data.get("history", []):
#                 st.write(f"**User Prompt:** {entry.get('prompt', '')}")
#                 st.write(f"**Response:** {entry.get('response', '')}")
#                 st.write("---")
                
#         except requests.exceptions.RequestException as e:
#             st.write("Error:", str(e))
#     else:
#         st.write("Please enter both User ID and input text.")

# 
# import streamlit as st
# import requests

# # URL of your Flask API
# FLASK_API_URL = "http://127.0.0.1:5000/api/query"

# # Streamlit app setup
# st.title("Groq.ai and Google Search Integration")

# # Input fields
# user_id = st.text_input("Enter your User ID")
# input_text = st.text_input("Search the topic you want")

# # Button to send request to Flask API
# if st.button("Submit"):
#     if user_id and input_text:
#         # Prepare the request payload
#         payload = {
#             "user_id": user_id,
#             "input_text": input_text
#         }
        
#         # Send POST request to Flask API
#         try:
#             response = requests.post(FLASK_API_URL, json=payload)
#             response.raise_for_status()
#             data = response.json()
            
#             # Display the Google search text results
#             st.write("**Google Search Text Results:**")
#             for result in data.get("text_results", []):
#                 st.write(f"**Title:** {result.get('title', 'No title')}")
#                 st.write(f"**Snippet:** {result.get('snippet', 'No snippet')}")
#                 st.write(f"**URL:** {result.get('link', 'No link')}")
#                 st.write("---")
            
#             # Display the Google search image results
#             st.write("**Google Search Image Results:**")
#             for image in data.get("image_results", []):
#                 st.image(image.get('thumbnail'), caption=image.get('link', 'No link'))
            
#             # Display the LLM response
#             st.write("**Groq Response:**")
#             st.write(data.get("llm_result", "No result available"))
            
#             # Display the chat history
#             st.write("**Chat History:**")
#             for entry in data.get("history", []):
#                 st.write(f"**User Prompt:** {entry.get('prompt', '')}")
#                 st.write(f"**Response:** {entry.get('response', '')}")
#                 st.write("---")
                
#         except requests.exceptions.RequestException as e:
#             st.write("Error:", str(e))
#     else:
#         st.write("Please enter both User ID and input text.")

# import streamlit as st
# import requests

# # URL of your Flask API
# FLASK_API_URL = "http://127.0.0.1:5000/api/query"

# # Streamlit app setup
# st.title("Groq.ai and Google Search Integration")

# # Input fields
# user_id = st.text_input("Enter your User ID")
# input_text = st.text_input("Search the topic you want")

# # Button to send request to Flask API
# if st.button("Submit"):
#     if user_id and input_text:
#         # Prepare the request payload
#         payload = {
#             "user_id": user_id,
#             "input_text": input_text
#         }
        
#         # Send POST request to Flask API
#         try:
#             response = requests.post(FLASK_API_URL, json=payload)
#             response.raise_for_status()
#             data = response.json()
            
#             # Display the Google search text results
#             st.write("**Google Search Text Results:**")
#             for result in data.get("text_results", []):
#                 st.write(f"**Title:** {result.get('title', 'No title')}")
#                 st.write(f"**Snippet:** {result.get('snippet', 'No snippet')}")
#                 st.write(f"**URL:** {result.get('link', 'No link')}")
#                 st.write("---")
            
#             # Display the Google search image results
#             st.write("**Google Search Image Results:**")
#             for image in data.get("image_results", [])[:5]:  # Only first 5 images
#                 st.image(image.get('thumbnail'), caption=image.get('link', 'No link'), width=200, use_column_width=False)
            
#             # Display the Google search video results
#             st.write("**Google Search Video Results:**")
#             for video in data.get("video_results", []):
#                 st.write(f"**Title:** {video.get('title', 'No title')}")
#                 st.write(f"**URL:** {video.get('link', 'No link')}")
#                 st.image(video.get('thumbnail'), width=200, use_column_width=False)
#                 st.write("---")
            
#             # Display the LLM response
#             st.write("**Groq Response:**")
#             st.write(data.get("llm_result", "No result available"))
            
#             # Display the chat history
#             st.write("**Chat History:**")
#             for entry in data.get("history", []):
#                 st.write(f"**User Prompt:** {entry.get('prompt', '')}")
#                 st.write(f"**Response:** {entry.get('response', '')}")
#                 st.write("---")
                
#         except requests.exceptions.RequestException as e:
#             st.write("Error:", str(e))
#     else:
#         st.write("Please enter both User ID and input text.")




# import streamlit as st
# import requests

# # URL of your Flask API
# FLASK_API_URL = "http://127.0.0.1:5000/api/query"

# # Streamlit app setup
# st.title("Groq.ai and Google Search Integration")

# # Input fields
# user_id = st.text_input("Enter your User ID")
# input_text = st.text_input("Search the topic you want")

# # Button to send request to Flask API
# if st.button("Submit"):
#     if user_id and input_text:
#         # Prepare the request payload
#         payload = {
#             "user_id": user_id,
#             "input_text": input_text
#         }
        
#         # Send POST request to Flask API
#         try:
#             response = requests.post(FLASK_API_URL, json=payload)
#             response.raise_for_status()
#             data = response.json()
            
#             # Display the Google search text results
#             st.write("**Google Search Text Results:**")
#             for result in data.get("text_results", []):
#                 st.write(f"**Title:** {result.get('title', 'No title')}")
#                 st.write(f"**Snippet:** {result.get('snippet', 'No snippet')}")
#                 st.write(f"**URL:** {result.get('link', 'No link')}")
#                 st.write("---")
            
#             # Display the Google search image results
#             st.write("**Google Search Image Results:**")
#             for image in data.get("image_results", [])[:5]:  # Only first 5 images
#                 st.image(image.get('thumbnail'), caption=image.get('link', 'No link'), width=200, use_column_width=False)
            
#             # Display the Google search video results
#             st.write("**Google Search Video Results:**")
#             for video in data.get("video_results", []):
#                 st.write(f"**Title:** {video.get('title', 'No title')}")
#                 st.write(f"**URL:** {video.get('link', 'No link')}")
#                 st.image(video.get('thumbnail'), width=200, use_column_width=False)
#                 st.write("---")

#             # Display the Google search related questions
#             st.write("**Google Search Related Questions:**")
#             for question in data.get("related_questions", []):
#                 st.write(f"**Question:** {question.get('question', 'No question')}")
#                 st.write(f"**Snippet:** {question.get('snippet', 'No snippet')}")
#                 st.write(f"**URL:** {question.get('link', 'No link')}")
#                 st.write("---")
            
#             # Display the LLM response
#             st.write("**Groq Response:**")
#             st.write(data.get("llm_result", "No result available"))
            
#             # Display the chat history
#             st.write("**Chat History:**")
#             for entry in data.get("history", []):
#                 st.write(f"**User Prompt:** {entry.get('prompt', '')}")
#                 st.write(f"**Response:** {entry.get('response', '')}")
#                 st.write("---")
                
#         except requests.exceptions.RequestException as e:
#             st.write("Error:", str(e))
#     else:
#         st.write("Please enter both User ID and input text.")

import streamlit as st
import requests

# URL of your Flask API
FLASK_API_URL = "http://127.0.0.1:5000/api/query"

# Streamlit app setup
st.title("Groq.ai and Google Search Integration")

# Input fields
user_id = st.text_input("Enter your User ID")
input_text = st.text_input("Search the topic you want")

# Button to send request to Flask API
if st.button("Submit"):
    if user_id and input_text:
        # Prepare the request payload
        payload = {
            "user_id": user_id,
            "input_text": input_text
        }
        
        # Send POST request to Flask API
        try:
            response = requests.post(FLASK_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Display the Google search text results
            st.write("**Google Search Text Results:**")
            for result in data.get("text_results", []):
                st.write(f"**Title:** {result.get('title', 'No title')}")
                st.write(f"**Snippet:** {result.get('snippet', 'No snippet')}")
                st.write(f"**URL:** {result.get('link', 'No link')}")
                st.write("---")
            
            # Display the Google search image results
            st.write("**Google Search Image Results:**")
            for image in data.get("image_results", [])[:5]:  # Only first 5 images
                if image.get('thumbnail'):
                    st.image(image.get('thumbnail'), caption=image.get('link', 'No link'), width=200, use_column_width=False)
            
            # Display the Google search video results
            st.write("**Google Search Video Results:**")
            for video in data.get("video_results", []):
                st.write(f"**Title:** {video.get('title', 'No title')}")
                st.write(f"**URL:** {video.get('link', 'No link')}")
                if video.get('thumbnail'):
                    st.image(video.get('thumbnail'), width=200, use_column_width=False)
                st.write("---")
            
            # Display the related questions
            st.write("**Related Questions:**")
            for question in data.get("related_questions", []):
                st.write(f"**Question:** {question.get('question', 'No question')}")
                st.write(f"**Answer:** {question.get('snippet', 'No answer')}")
                st.write(f"**URL:** {question.get('link', 'No link')}")
                st.write("---")

            # Display the LLM response
            st.write("**Groq Response:**")
            st.write(data.get("llm_result", "No result available"))
            
            # Display the chat history
            st.write("**Chat History:**")
            for entry in data.get("history", []):
                st.write(f"**User Prompt:** {entry.get('prompt', '')}")
                st.write(f"**Response:** {entry.get('response', '')}")
                st.write("---")
                
        except requests.exceptions.RequestException as e:
            st.write("Error:", str(e))
    else:
        st.write("Please enter both User ID and input text.")
