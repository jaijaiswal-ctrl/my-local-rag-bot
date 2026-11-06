#  ChatWithMyPDF: A Private, Local AI Knowledge Base

### "Stop guessing. Start knowing."

Ever tried asking an AI about a specific document, only for it to make up a convincing but totally fake answer? That's called a hallucination. I built **ChatWithMyPDF** to solve that. 

This project is a **RAG (Retrieval-Augmented Generation)** system. Instead of relying on what the AI "thinks" it knows, this app forces the AI to read your actual PDF, find the exact paragraph containing the answer, and summarize it for you. 

The best part? **It's 100% local.** No API keys, no monthly subscriptions, and your private documents never leave your Mac.

---

##  How it Works (In Plain English)

I've designed the app to follow a simple four-step process:
1. **The Eyes (Extraction):** It uses `PyMuPDF` to rip the text out of your PDF with high precision.
2. **The Slicer (Chunking):** Because AI can't read 100 pages at once, the app slices the text into small, overlapping chunks so no context is lost.
3. **The Memory (Vector DB):** Using `nomic-embed-text`, it turns those text chunks into mathematical vectors and stores them in `ChromaDB`.
4. **The Brain (Generation):** When you ask a question, the app searches the memory for the most relevant chunks and feeds them to **Llama 3.1** to generate a grounded, accurate answer.

---

##  The Tech Stack

- **LLM:** Llama 3.1 (via Ollama)
- **Embeddings:** nomic-embed-text (via Ollama)
- **Vector Database:** ChromaDB
- **PDF Engine:** PyMuPDF
- **Frontend:** Streamlit
- **Language:** Python 3.9+

---

##  Getting Started

Since this app runs locally, you'll need to set up the "AI Engine" first.

### 1. Install Ollama
First, download and install [Ollama](https://ollama.com). Once installed, open your terminal and pull the two models I used for this project:
```bash
ollama pull llama3.1
ollama pull nomic-embed-text


###Clone & Setup
Clone this repository to your machine and navigate into the folder:

git clone https://github.com/YOUR_USERNAME/my-local-rag-bot.git
cd my-local-rag-bot


###Create your Environment
I highly recommend using a virtual environment to keep your Mac clean:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


###How to Use
Launch the App: In your terminal, run:
                 streamlit run web_app.py
Upload your PDF: Once the website opens in your browser, use the sidebar to upload any PDF file.

Process the Document: Click the "Process Document" button. The AI will read the PDF and create a local memory database.

Start Chatting: Ask any question in the chat box! You can even click the "View Sources" dropdown to see exactly which part of the PDF the AI used to find the answer


###Note for Mac Users
This project is optimized for Apple Silicon (M1, M2, M3, M4, M5). Thanks to Unified Memory, the models run incredibly fast and entirely on your GPU.

Happy Chatting! 


***

###  Pro-Tips for your GitHub Profile:
1. **Replace `YOUR_USERNAME`**: In the "Clone & Setup" section, make sure you put your actual GitHub username in the link.
2. **Add a Screenshot**: If you want your GitHub to look amazing, take a screenshot of your Streamlit website, upload the image to your GitHub folder, and add this line to the top of the README:
   `![App Screenshot](screenshot.png)`
3. **The "About" Section**: On the right side of your GitHub repository page, add a description like: *"A local RAG system to chat with PDFs using Llama 3.1 and ChromaDB. 100% Private. 100% Local."*

**You are now ready to `git push`!** 