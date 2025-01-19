import gradio as gr
from serpapi import GoogleSearch
import os
import requests
import json

# Configure your API keys
SERPAPI_API_KEY = "d3f3bf77167951c1aec4a56a46590a7ff760653a09662a547bd59a073f96523a"
GEMINI_API_KEY = "AIzaSyDX10JHWr3HSGtE5r_pMky73bl7NQ_xGnU"

def web_search(query):
    """Perform web search using SerpAPI"""
    search = GoogleSearch({
        "q": query,
        "num": 5,  # Number of results to retrieve
        "location_requested": "Ankara, Turkiye",
        "location_used": "Ankara,Turkiye",
        "google_domain": "google.com.tr",
        "api_key": SERPAPI_API_KEY
    })
    results = search.get_dict()
    
    # Extract relevant information from search results and remove duplicates
    
    search_results = []
    
    search_results = []
    for result in results.get("organic_results", []):
        search_results.append({
            "title": result.get("title", ""),
            "snippet": result.get("snippet", ""),
            "link": result.get("link", "")
        })
    return search_results

def format_search_results(results):
    """Format search results for the model input"""
    formatted_text = "Search Results:\n\n"
    for idx, result in enumerate(results, 1):
        formatted_text += f"{idx}. {result['title']}\n"
        formatted_text += f"   {result['snippet']}\n"
        formatted_text += f"   Source: {result['link']}\n\n"
    return formatted_text

def postprocess_response(response):
    """Process the response to ensure unique links"""
    # Split the response into main content and sources if sources exist
    parts = response.split("Sources:", 1)
    
    if len(parts) == 2:
        main_content, sources = parts
        # Extract links from the sources section
        lines = sources.strip().split('\n')
        unique_links = []
        seen_links = set()
        
        for line in lines:
            # Look for URLs in the line
            if "http" in line.lower():
                # Don't add if we've seen this link before
                if line.strip() not in seen_links:
                    seen_links.add(line.strip())
                    unique_links.append(line.strip())
        
        # Reconstruct the response with unique links
        if unique_links:
            return f"{main_content}\n\nSources:\n" + "\n".join(unique_links)
    
    return response

def call_gemini_api(system_prompt, prompt):
    """Call Gemini 1.5 Flash API directly"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{system_prompt} {prompt}"
            }]
        }],
        "generation_config": {
            "temperature": 1,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024
        },
        "safety_settings": [{
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        
        if response_data.get("candidates") and response_data["candidates"][0].get("content"):
            generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            # Process the response to ensure unique links
            return postprocess_response(generated_text)
        else:
            return "Error: Unable to extract response from API"
            
    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid response from API"

def generate_response(user_query):
    """Generate response using search results and Gemini API"""
    try:
        # Perform web search
        search_results = web_search(user_query)
        
        # Format context for the model
        search_context = format_search_results(search_results)
        
        system_prompt = """Based on the search results, understand the intent of the user and provide a comprehensive and accurate response to the query. 
                        Include relevant information from the sources while maintaining a natural, conversational tone.
                        After your response, list the sources under a 'Sources:' heading. Each source should be listed only once."""

        # Prepare prompt for Gemini
        prompt = f"Query: {user_query} Search result: {search_context}"

        # Generate response using Gemini
        return call_gemini_api(system_prompt, prompt)

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
def gradio_interface(query):
    return generate_response(query)

# Define and launch the Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="Enter your question", placeholder="What would you like to know?", lines=2)
    ],
    outputs=gr.Textbox(label="Response", lines=10),
    title="Search-Enhanced Question Answering with Gemini 1.5 Flash",
    description="Ask any question and get an AI-generated response based on current web search results.",
    examples=[
        ["Where does Egemen Doruk Serdar study at?"],
        ["Which company does Berke Cem Oktem work for?"],
        ["Which company does Irem Besiroglu intern for?"]
    ]
)

if __name__ == "__main__":
    iface.launch(share=True)