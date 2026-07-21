# 🎥 AI Video Assistant

> **Transform YouTube videos into searchable knowledge with AI-powered summarization, transcription, and conversational insights.**

![AI Video Assistant Demo](https://via.placeholder.com/800x400?text=AI+Video+Assistant+Dashboard)

## ✨ Features

- **📥 YouTube Video Processing**: Download and extract audio from YouTube URLs
- **🎙️ Advanced Transcription**: Powered by OpenAI Whisper for accurate speech-to-text
- **📝 AI-Powered Summarization**: Concise, professional summaries using Mistral AI
- **🎯 Insight Extraction**: Automatically identify action items, key decisions, and open questions
- **💬 Conversational AI Chat**: Ask questions about video content using Retrieval-Augmented Generation (RAG)
- **🎨 Modern SaaS-Style Interface**: Beautiful gradient animations, glassmorphism cards, and interactive elements
- **📊 Insight Dashboard**: Visual metrics and organized tabs for easy navigation
- **💾 Export Capabilities**: Download summaries and transcripts
- **🔒 Privacy-Focused**: All processing happens locally (except API calls to Whisper and Mistral)

## 🚀 How It Works

1. **Input**: Paste a YouTube URL or upload a video/audio file
2. **Process**: 
   - Audio extraction using yt-dlp and FFmpeg
   - Speech-to-text transcription with Whisper
   - Text chunking and embedding generation
   - Vector storage in ChromaDB for semantic search
3. **Output**:
   - AI-generated summary and title
   - Extracted action items, decisions, and questions
   - Interactive chat interface for contextual Q&A
4. **Interaction**: Ask natural language questions about the video content and get accurate, cited responses

## 🛠️ Technology Stack

| Category      | Technologies                                                                 |
|---------------|------------------------------------------------------------------------------|
| **Frontend**  | Streamlit (with custom CSS animations and glassmorphism)                     |
| **Backend**   | Python                                                                       |
| **AI/ML**     | Mistral AI (LLM), OpenAI Whisper (Speech-to-Text)                            |
| **Embeddings**| HuggingFace BGE (`all-MiniLM-L6-V2`)                                         |
| **Vector DB** | ChromaDB                                                                     |
| **Audio**     | yt-dlp, FFmpeg, Pydub                                                        |
| **Processing**| LangChain (LCEL framework for chaining operations)                           |

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Video-Assistant.git
   cd AI-Video-Assistant
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

5. **Download required models**
   The app will automatically download:
   - Whisper model (base/small/medium/large)
   - Sentence transformer model for embeddings

6. **Run the application**
   ```bash
   streamlit run appz.py
   ```

7. **Open in browser**
   Visit `http://localhost:8501` to access the interface

## 🎨 UI Features

- **Animated Gradient Background**: Smoothly shifting color gradients
- **Glassmorphism Design**: Frosted glass effects with backdrop blur
- **Interactive Elements**: Hover animations, pulse effects, and micro-interactions
- **Responsive Layout**: Works on desktop and tablet screens
- **Dark Mode Optimized**: Designed for dark backgrounds with vibrant accents
- **Modern Typography**: Clean, readable font hierarchy
- **Fluid Transitions**: Smooth state changes and loading indicators

## 📱 Screenshots

![Hero Section](https://via.placeholder.com/800x400?text=Hero+Section+with+Animated+Gradient)
![Analysis Dashboard](https://via.placeholder.com/800x400?text=Analysis+Dashboard+with+Metrics)
![Chat Interface](https://via.placeholder.com/800x400?text=Conversational+AI+Chat)

## ⚙️ Configuration

### Environment Variables
| Variable           | Description                          | Default          |
|--------------------|--------------------------------------|------------------|
| `MISTRAL_API_KEY`  | API key for Mistral AI services      | *(required)*     |
| `WHISPER_MODEL`    | Whisper model size (tiny, base, small, medium, large) | `small` |

### Audio Processing
- Chunk size: 10 minutes (configurable in `utils/audio_processor.py`)
- Output format: 16kHz mono WAV for optimal Whisper performance

## 📝 Usage Examples

### Educational Content
- Convert lecture videos into searchable study guides
- Extract key concepts and create flashcards from explanations
- Generate summaries for quick review before exams

### Business Meetings
- Automatically capture action items and decisions
- Search meeting transcripts for specific topics or decisions
- Create follow-up emails based on extracted commitments

### Research & Development
- Analyze conference talks and technical presentations
- Extract methodology and results from academic videos
- Build a knowledge base of industry expert interviews

### Content Creation
- Repurpose video content into blog posts or social media
- Identify quotable moments for highlights reels
- Research competitor content and extract key points

## 🔧 Development

### Project Structure
```
AI-Video-Assistant/
├── appz.py                 # Main Streamlit application
├── main.py                 # Core processing pipeline
├── requirements.txt        # Python dependencies
├── style.css               # Custom styling with animations
├── readme.md               # This file
├── .env                    # Environment variables (not tracked)
├── core/
│   ├── transcriber.py      # Whisper integration
│   ├── summarizer.py       # Mistral-based summarization
│   ├── extractor.py        # Action item/decision/question extraction
│   ├── rag_engine.py       # RAG pipeline with ChromaDB
│   └── vector_store.py     # Vector database operations
├── utils/
│   └── audio_processor.py  # Audio download and conversion
├── downloads/              # Temporary audio storage
└── vector_db/              # ChromaDB persistence
```

### Extending Functionality
- **Add new LLMs**: Modify `get_llm()` functions in core modules
- **Change embedding model**: Update `EMBEDDING_MODEL` in `vector_store.py`
- **Adjust chunking**: Modify chunk size in `summarizer.py` and `vector_store.py`
- **Add new export formats**: Extend the download buttons in `appz.py`

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Streamlit](https://streamlit.io) for the amazing frontend framework
- [LangChain](https://www.langchain.com) for simplifying LLM orchestration
- [OpenAI Whisper](https://github.com/openai/whisper) for state-of-the-art speech recognition
- [Mistral AI](https://mistral.ai) for powerful open-weight language models
- [Hugging Face](https://huggingface.co) for accessible embedding models
- [ChromaDB](https://www.trychroma.com) for efficient vector storage

## 🙋‍♂️ Support

For questions, feature requests, or contributions:
- Open an issue on GitHub
- Contact the maintainer: [priyansh pal](https://www.linkedin.com/in/priyans-pal-0b1006263/)
- Star the repository if you find it useful!

---

<div align="center">
  Made with ❤️ for knowledge workers, researchers, and lifelong learners
</div>