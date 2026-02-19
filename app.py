import streamlit as st
import os
from dotenv import load_dotenv
from brain import get_index_for_pdf
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load Environment Variables
load_dotenv()
# Make sure you have GOOGLE_API_KEY=AIzaSy... in your .env file
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

st.title("RAG enhanced Chatbot (Gemini Edition)")

@st.cache_data
def create_vectordb(files, filenames):
    with st.spinner("Creating Vector Database..."):
        # We pass the Google API Key to the brain for embeddings
        vectordb = get_index_for_pdf(
            [file.getvalue() for file in files], filenames, api_key
        )
    return vectordb

pdf_files = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)

if pdf_files:
    pdf_file_names = [file.name for file in pdf_files]
    st.session_state["vectordb"] = create_vectordb(pdf_files, pdf_file_names)

prompt_template = """
    You are a helpful Assistant who answers users' questions based on multiple contexts given to you.
    Keep your answer short and to the point.
    The evidence is the context of the pdf extract with metadata. 
    Carefully focus on the metadata specially 'filename' and 'page' whenever answering.
    Make sure to add filename and page number at the end of the sentence you are citing.
    Reply "Not applicable" if the text is irrelevant.
    
    The PDF content is:
    {pdf_extract}
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask anything")

if question:
    vectordb = st.session_state.get("vectordb", None)
    if not vectordb:
        st.error("Please upload a PDF first.")
        st.stop()

    # Display user question
    with st.chat_message("user"):
        st.write(question)
    st.session_state["messages"].append({"role": "user", "content": question})

    # RAG Logic: Search for context
    search_results = vectordb.similarity_search(question, k=3)
    pdf_extract = "\n".join([result.page_content for result in search_results])
    
    # Construct the final prompt for Gemini
    full_prompt = prompt_template.format(pdf_extract=pdf_extract) + f"\n\nUser Question: {question}"

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(full_prompt)
            result = response.content
            st.write(result)

    # Store assistant response
    st.session_state["messages"].append({"role": "assistant", "content": result})