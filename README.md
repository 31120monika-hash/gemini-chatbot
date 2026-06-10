# Gemini AI Chatbot

A simple Streamlit chatbot using LangChain for conversation memory and the Google Gemini API for answer generation.

## Features

- Streamlit-based interactive chat UI
- LangChain `ConversationBufferMemory` for ongoing conversation context
- Gemini API via direct HTTP requests
- Secure API key configuration with `.env`
- Error handling for API issues and missing credentials

## Project Structure

- `app.py` — Streamlit application and user interface
- `chatbot.py` — Gemini LLM wrapper and LangChain conversation chain
- `requirements.txt` — Python dependencies
- `.env.example` — example environment variables
- `.gitignore` — ignores Python caches and `.env`

## Usage

- Type a question into the input field.
- Click **Send**.
- The chatbot will respond and preserve prior conversation history.

## Notes

- If you need a different Gemini model, update `GEMINI_MODEL` in `.env`.
- Keep your `.env` file private and do not commit it to version control.
"# gemini-chatbot" 

## Troubleshooting

### Model Not Found Error
You may encounter:

