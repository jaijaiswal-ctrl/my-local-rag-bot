import ollama
import chromadb
from pypdf import PdfReader

def read_pdf(file_path):
    print("Reading PDF...")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

def slice_text(text):
    chunk_size = 500 
    overlap = 100 
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# --- MEMORY SYSTEM WITH FIX ---
db_client = chromadb.PersistentClient(path="./my_ai_memory")

# Hard reset the memory to avoid the 'where={}' error
try:
    db_client.delete_collection(name="my_docs")
    print("Old memory cleared.")
except:
    pass 

collection = db_client.get_or_create_collection(name="my_docs")

# --- LOADING KNOWLEDGE ---
pdf_text = read_pdf("data.pdf") 
chunks = slice_text(pdf_text)

print(f"Processing {len(chunks)} pieces of information with overlap...")
for i, chunk in enumerate(chunks):
    embedding = ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
    collection.add(ids=[str(i)], embeddings=[embedding], documents=[chunk])

print("Memory updated for higher accuracy!")

def ask_llama(question):
    q_emb = ollama.embeddings(model="nomic-embed-text", prompt=question)["embedding"]
    
    # Get top 5 chunks for better accuracy
    results = collection.query(query_embeddings=[q_emb], n_results=5)
    context = "\n\n---\n\n".join(results['documents'][0])
    
    prompt = f"""
    You are a precise research assistant. Use the provided context to answer the question.
    
    RULES:
    1. Use ONLY the context provided. 
    2. If the answer is not in the context, say "I cannot find the answer in the document."
    3. Do not use your outside knowledge.
    4. Be detailed and cite the specific part of the text if possible.

    CONTEXT:
    {context}

    QUESTION: 
    {question}

    FINAL ANSWER:
    """
    
    response = ollama.generate(model="llama3.1", prompt=prompt)
    return response['response']

print("\n--- High-Accuracy Mode Ready! ---")
while True:
    user_q = input("\nYour Question: ")
    if user_q.lower() in ['quit', 'exit', 'bye']:
        break
    print("Llama 3.1 is analyzing...")
    answer = ask_llama(user_q)
    print(f"\nAI: {answer}")
