import re
import streamlit as st
from io import BytesIO
from typing import Tuple, List

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS 
from pypdf import PdfReader

def parse_pdf(file: BytesIO, filename: str) -> Tuple[List[str], str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            # Clean up hyphenation and newlines
            text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
            text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
            text = re.sub(r"\n\s*\n", "\n\n", text)
            output.append(text)
    return output, filename

def text_to_docs(text: List[str], filename: str) -> List[Document]:
    if isinstance(text, str):
        text = [text]
    
    # Create initial page-level documents
    page_docs = [Document(page_content=page, metadata={"page": i + 1}) for i, page in enumerate(text)]

    doc_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        chunk_overlap=200, 
    )
    
    for doc in page_docs:
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            new_doc = Document(
                page_content=chunk, 
                metadata={
                    "page": doc.metadata["page"], 
                    "chunk": i,
                    "source": f"{doc.metadata['page']}-{i}",
                    "filename": filename
                }
            )
            doc_chunks.append(new_doc)
    return doc_chunks

def docs_to_index(docs, google_api_key):
    # 1. FIX for IndexError: Check if the document list is empty
    if not docs:
        st.error("No text could be extracted from this PDF. It might be a scanned image or encrypted.")
        st.stop() # Stops execution to prevent the FAISS crash

    # 2. Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=google_api_key
    )
    
    # 3. Create the FAISS index
    index = FAISS.from_documents(docs, embeddings)
    return index

def get_index_for_pdf(pdf_files, pdf_names, google_api_key):
    documents = []
    for pdf_file, pdf_name in zip(pdf_files, pdf_names):
        text, filename = parse_pdf(BytesIO(pdf_file), pdf_name)
        new_docs = text_to_docs(text, filename)
        documents.extend(new_docs)
    
    # Pass the Google API Key to the indexer
    index = docs_to_index(documents, google_api_key)
    return index