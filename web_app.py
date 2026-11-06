import streamlit as st
import ollama
import chromadb
from pypdf import PdfReader
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro AI Document Bot", page_icon="🤖", layout="wide")
st.title("🤖 Pro Chat with your PDF")
st.markdown("### High-Accuracy Mode Enabled")

# --- CORE FUNCTIONS ---
import fitz  # This is PyMuPDF

def read_pdf(file):
    # We read the file bytes and open it with fitz
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") # This is much more accurate than pypdf
    return text


def slice_text(text):
    # UPGRADE: Increased chunk size to 1000 for better context
    chunk_size = 1000 
    overlap = 200 
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# --- INITIALIZE DATABASE ---
if "db_client" not in st.session_state:
    st.session_state.db_client = chromadb.PersistentClient(path="./my_ai_memory")
    st.session_state.collection = st.session_state.db_client.get_or_create_collection(name="web_docs")

# --- SIDEBAR: PDF UPLOAD ---
with st.sidebar:
    st.header("Documents")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file:
        if st.button("Process Document"):
            with st.spinner("Indexing..."):
                try:
                    st.session_state.db_client.delete_collection(name="web_docs")
                except:
                    pass
                
                collection = st.session_state.db_client.get_or_create_collection(name="web_docs")
                text = read_pdf(uploaded_file)
                chunks = slice_text(text)
                
                for i, chunk in enumerate(chunks):
                    emb = ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
                    collection.add(ids=[str(i)], embeddings=[emb], documents=[chunk])
                
                st.success("Indexing Complete!")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a specific question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching document..."):
            # 1. Retrieval
            q_emb = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
            collection = st.session_state.db_client.get_collection(name="web_docs")
            
            # We grab top 5 chunks
            results = collection.query(query_embeddings=[q_emb], n_results=5)
            retrieved_docs = results['documents'][0]
            context = "\n\n---\n\n".join(retrieved_docs)
            
            # --- DEBUG WINDOW: SEE WHAT THE AI SEES ---
            with st.expander("🔍 View Sources (What the AI is reading)"):
                for i, doc in enumerate(retrieved_docs):
                    st.markdown(f"**Source {i+1}:**\n{doc}")
                    st.divider()
            
            # 2. Generation (Hyper-Strict Prompt)
            full_prompt = f"""
            You are an expert document analyzer. Your goal is to provide a 100% accurate answer based ONLY on the provided context.
            
            STRICT RULES:
            1. If the answer is not explicitly written in the context, say: "I am sorry, but the document does not contain this information."
            2. Do NOT use any outside knowledge.
            3. Do NOT hallucinate or guess.
            4. Use bullet points for clarity if the answer is long.
            
            CONTEXT: 
            {context}
            
            QUESTION: 
            {prompt}
            
            ACCURATE ANSWER:
            """
            response = ollama.generate(model="llama3.1", prompt=full_prompt)
            answer = response['response']
            
            st.markdown(answer)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})
