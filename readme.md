# 🎥 AI Video Assistant with RAG

An intelligent AI-powered Video Assistant that transforms YouTube videos into searchable knowledge. The application automatically downloads videos, extracts audio, generates transcripts, creates AI-powered summaries, extracts action items, and enables users to ask context-aware questions using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📥 Download audio from YouTube videos
- 🎙️ Automatic speech-to-text transcription
- 📝 AI-generated video summaries
- ✅ Automatic extraction of key action items
- 🔍 Retrieval-Augmented Generation (RAG) for contextual question answering
- 🧠 Semantic search using ChromaDB Vector Database
- 💬 Interactive chatbot for video-based conversations
- 📊 Clean and responsive Streamlit interface
- ⚡ Fast document retrieval using embeddings

---

## 📸 Application Workflow

```
YouTube URL
      │
      ▼
Download Audio (yt-dlp)
      │
      ▼
Audio Extraction (FFmpeg)
      │
      ▼
Speech-to-Text Transcription
      │
      ▼
Text Chunking
      │
      ▼
Embeddings Generation
      │
      ▼
Chroma Vector Database
      │
      ▼
      RAG
      │
      ▼
Question Answering
      │
      ├── Video Summary
      ├── Action Items
      └── Chat with Video
```

---

# 🛠️ Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### AI & LLM

- Mistral AI
- LangChain
- Retrieval-Augmented Generation (RAG)

### Vector Database

- ChromaDB

### Audio Processing

- yt-dlp
- FFmpeg
- Pydub

### Embeddings

- LangChain Embeddings

### Other Libraries

- Pandas
- NumPy
- OS
- dotenv

---

# 📂 Project Structure

```
AI-VIDEO-ASSISTANT
│
├── app.py
├── main.py
├── requirements.txt
├── style.css
├── .gitignore
│
├── core
│   ├── extractor.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils
│   └── audio_processing.py
│
├── downloads/
├── vector_db/
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Video-Assistant.git
```

Move into the project directory

```bash
cd AI-Video-Assistant
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate the environment

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside the project root.

Example:

```env
MISTRAL_API_KEY=YOUR_API_KEY
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

Open your browser

```
http://localhost:8501
```

---

# 💡 How It Works

### Step 1

Paste a YouTube video URL.

### Step 2

The application downloads the video's audio.

### Step 3

Speech is converted into text using the transcription pipeline.

### Step 4

The transcript is split into semantic chunks.

### Step 5

Embeddings are generated for each chunk.

### Step 6

The embeddings are stored in ChromaDB.

### Step 7

The user can:

- Generate an AI summary
- View action items
- Ask questions about the video
- Retrieve context-aware answers using RAG

---

# 🧠 RAG Pipeline

```
Transcript
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Retriever
      │
      ▼
Relevant Context
      │
      ▼
Mistral LLM
      │
      ▼
Final Response
```

---

# 📌 Example Use Cases

- Educational lecture summarization
- Meeting recordings
- Online course notes
- Podcast analysis
- Interview summarization
- Research videos
- Product reviews
- Conference talks

---

# 📈 Future Improvements

- Multiple LLM support (OpenAI, Gemini, Claude)
- PDF export
- Multi-language transcription
- Speaker diarization
- Video timestamp citations
- Cloud deployment
- Authentication
- Chat history
- Multiple video knowledge base
- OCR support for slides
- Voice-based interaction

---

# 📷 Screenshots

Add screenshots here.

Example:

```
images/home.png

images/chat.png

images/summary.png
```

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create your feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Priyansh Pal**

LinkedIn:
https://www.linkedin.com/in/priyans-pal-0b1006263/

GitHub:
https://github.com/dopaminechillzz

---

## ⭐ If you found this project helpful, please consider giving it a Star!