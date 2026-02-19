# RAG Chatbot with Gemini

A Retrieval Augmented Generation (RAG) chatbot built with LangChain, Streamlit, and Google's Gemini API.

**🚀 [Live Demo -https://raggemini-sgydghhwunzcauwdn7b3bh.streamlit.app/]
)**

## Features

- 📄 Upload and process multiple PDF files
- 🤖 AI-powered responses using Google Gemini 1.5 Flash
- 🔍 Semantic search with FAISS vector store
- 📍 Source citations with file names and page numbers
- 💬 Multi-turn conversation support

## Project Structure

- `app.py` - Streamlit frontend interface
- `brain.py` - PDF processing and vector database management
- `.env` - Environment variables (API keys)
- `requirements.txt` - Python dependencies

## Quick Start

### Local Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Ankitsingh2820/Rag_gemini.git
cd Rag_gemini
```

2. **Create a virtual environment**:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up your Google API key**:
   - Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
   - Create a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. **Run the app**:
```bash
.\venv\Scripts\streamlit.exe run app.py
```

Access at `http://localhost:8502`

## Deploy on Streamlit Cloud

1. **Repository is ready** ✓ (https://github.com/Ankitsingh2820/Rag_gemini)

2. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select:
     - Repository: `Ankitsingh2820/Rag_gemini`
     - Branch: `master`
     - Main file: `app.py`

3. **Add Secrets**:
   - Go to app settings → "Secrets"
   - Add your API key:
   ```
   GOOGLE_API_KEY = "your_api_key_here"
   ```

4. **Deploy** - Streamlit will automatically deploy your app!

Your live app URL will be something like: `https://rag-chatbot-gemini.streamlit.app`

## How It Works

1. Upload PDF files through the web interface
2. PDFs are parsed into chunks and converted to embeddings
3. Embeddings are stored in a FAISS vector database
4. When you ask a question, it's embedded and matched against stored documents
5. Similar contexts are sent to Gemini along with your question
6. Gemini generates an answer with source citations (file name + page number)

## Technologies

- **LangChain** - LLM framework for RAG
- **Streamlit** - Web app framework
- **Google Gemini API** - LLM
- **FAISS** - Vector similarity search
- **PyPDF** - PDF parsing

## Requirements

- Python 3.8+
- Google API key (free from [ai.google.dev](https://ai.google.dev))

## License

MIT License

## Support

For issues or questions, please create an issue on [GitHub](https://github.com/Ankitsingh2820/Rag_gemini/issues).
