# from flask import Flask, request
# from twilio.twiml.messaging_response import MessagingResponse
# from google import search

# #from googlesearch import search
# #from GoogleSearch import GoogleSearch
# #from serpapi import googlesearch


# app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# def bot():
#     # Get the user's message
#     user_msg = request.values.get('Body', '').lower()
    
#     # Create the response object
#     response = MessagingResponse()
    
#     # If the user message is empty, ask them to input something
#     if not user_msg:
#         msg = response.message("Please send a query, e.g., 'I want to learn about machine learning.'")
#     else:
#         # Search query with user message and a website for context (you might replace this with a different logic)
#         query = user_msg + " site:geeksforgeeks.org"
        
#         # Search for the query
#         result = []
#         for url in search(query, num=5, stop=5, pause=2):
#             result.append(url)
        
#         # Respond with the results
#         msg = response.message(f"--- Results for '{user_msg}' ---")
#         for url in result:
#             msg.body(url)  # Add each URL to the response
    
#     return str(response)

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

# Initialize the Flask application
app = Flask(__name__)

# Function to search DuckDuckGo API and return related topics for a query
def search_duckduckgo(query):
    url = "https://api.duckduckgo.com/"  # DuckDuckGo API endpoint
    params = {
        'q': query,      # Query string for DuckDuckGo search
        'format': 'json', # Requesting response in JSON format
    }
    
    try:
        # Send the request to DuckDuckGo API
        response = requests.get(url, params=params, timeout=5)  # 5-second timeout
        
        # Check if the response status is OK (200)
        if response.status_code == 200:
            results = response.json()  # Parse the JSON response
            return results.get('RelatedTopics', [])  # Extract related topics
        else:
            return None  # Return None if the status code is not 200 (error case)
    except requests.exceptions.RequestException as e:
        # Handle any request errors (e.g., timeout, connection issue)
        print(f"Error during request to DuckDuckGo API: {e}")
        return None

# Define a route that handles POST requests to '/webhook'
@app.route('/webhook', methods=['POST'])
def home():
    return bot()  # Call the bot function when the '/webhook' route is triggered

# Function to handle the incoming user message, process it, and return the bot's response
def bot():
    # Get the user's message (in lowercase for case-insensitive comparison)
    user_msg = request.values.get('Body', '').lower()
    
    # Create a MessagingResponse object to build the reply
    response = MessagingResponse()
    
    if not user_msg:
        # If there's no message, ask the user to send a query
        msg = response.message("Please send a query, e.g., 'I want to learn about machine learning.'")
    else:
        # Call DuckDuckGo API to search for related topics
        related_topics = search_duckduckgo(user_msg)
        
        if related_topics:
            # If there are related topics, send a message with the results
            msg = response.message(f"--- Results for user query '{user_msg}' ---")
            
            # Limit results to 3 topics for brevity
            max_results = 3
            for idx, topic in enumerate(related_topics[:max_results]):  # Slice to limit results
                if 'Text' in topic:
                    msg.body(f"{idx + 1}. {topic['Text']}")
                if 'FirstURL' in topic:
                    msg.body(f"Link: {topic['FirstURL']}")
        else:
            # If no results, notify the user
            msg = response.message("Sorry, I couldn't find anything related to your query.")
    
    return str(response)

# Start the Flask server with debugging enabled (host is 0.0.0.0 to accept connections from all network interfaces)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

#tracking additional changes
#more 





