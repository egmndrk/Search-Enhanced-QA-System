# Search-Enhanced Question Answering System with Gemini 1.5 Flash

A web application that combines Google Search results with Gemini 1.5 Flash's powerful language model to provide comprehensive answers to user queries. The system fetches real-time search results and uses them as context to generate accurate, up-to-date responses.

## Features

- Real-time web search integration using SerpAPI
- Advanced question answering using Google's Gemini 1.5 Flash model
- User-friendly interface built with Gradio
- Automatic deduplication of sources
- Location-based search results (currently set to Ankara, Turkey)
- Easy-to-use web interface with example queries

## Prerequisites

Before running this application, you'll need:

- Python 3.7 or higher
- SerpAPI API key (for web search functionality)
- Gemini API key (for the language model)

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
Replace the placeholder API keys in `hello.py` with your actual API keys:
```python
SERPAPI_API_KEY = "your_serpapi_key_here"
GEMINI_API_KEY = "your_gemini_key_here"
```

**Note:** It's recommended to use environment variables for API keys in production environments.

## Usage

1. Run the application:
```bash
python hello.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://127.0.0.1:7860`)

3. Enter your question in the text box and submit

4. The system will:
   - Search the web for relevant information
   - Process the search results
   - Generate a comprehensive response using Gemini 1.5 Flash
   - Display the response along with sources

## Configuration

You can modify the following parameters in the code:

- Number of search results (`num` parameter in `web_search` function)
- Search location (`location_requested` and `location_used` in `web_search` function)
- Google domain for search (`google_domain` in `web_search` function)
- Gemini model parameters (temperature, top_p, top_k, etc. in `call_gemini_api` function)

## API Response Processing

The system includes several processing steps:
- Removes duplicate sources from responses
- Formats search results for optimal context
- Ensures proper citation of sources in the final output

## Example Queries

The application comes with pre-configured example queries:
- "Where does Egemen Doruk Serdar study at?"
- "Which company does Berke Cem Oktem work for?"
- "Which company does Irem Besiroglu intern for?"

## Error Handling

The application includes error handling for:
- API request failures
- Invalid API responses
- General exceptions during execution

## Security Notes

- Never commit API keys to version control
- Consider implementing rate limiting for production use
- Monitor API usage to prevent excessive costs

## Disclaimer

This project uses third-party APIs (SerpAPI and Gemini) that may have associated costs. Please review their pricing and terms of service before deployment.
