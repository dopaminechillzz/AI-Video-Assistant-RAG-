import time
import tempfile

import streamlit as st

# -------------------------
# Your AI Pipeline
# -------------------------
from main import run_pipeline
from core.rag_engine import ask_question

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="VideoAssist - AI Video Analysis",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Load CSS
# -------------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =====================================================
# YOUTUBE-STYLE HEADER
# =====================================================
st.markdown(
    """
    <header class="yt-header">
        <div class="yt-header-left">
            <div class="yt-logo">
                <svg class="yt-logo-icon" viewBox="0 0 24 24" width="32" height="32">
                    <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0C.488 3.45.029 5.804 0 12c.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0C23.512 20.55 23.971 18.196 24 12c-.029-6.185-.484-8.549-4.385-8.816zM9 16V8l8 4-8 4z" fill="#FF0000"/>
                </svg>
                <span class="yt-logo-text">Video<span>Assist</span></span>
            </div>
        </div>
        <div class="yt-header-right">
            <a class="yt-nav-link" href="https://github.com/master-priyansh/F--AI-VIDEO-AGENT" target="_blank">GitHub</a>
        </div>
    </header>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# Session State
# =====================================================
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_upload" not in st.session_state:
    st.session_state.show_upload = False

if "video_url" not in st.session_state:
    st.session_state.video_url = ""


# =====================================================
# WELCOME / HERO (shown only before first analysis)
# =====================================================
if not st.session_state.result:
    st.markdown(
        """
        <div class="welcome-section">
            <svg class="yt-logo-icon" viewBox="0 0 24 24" width="48" height="48" style="margin-bottom:16px;">
                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0C.488 3.45.029 5.804 0 12c.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0C23.512 20.55 23.971 18.196 24 12c-.029-6.185-.484-8.549-4.385-8.816zM9 16V8l8 4-8 4z" fill="#FF0000"/>
            </svg>
            <h1 class="welcome-title">Analyze any video with AI</h1>
            <p class="welcome-subtitle">Paste a YouTube link to get AI-powered summaries, transcripts, insights, and more.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# SEARCH BAR — YouTube Style (centered)
# =====================================================
# Wrap search in centered columns
left_spacer, search_area, right_spacer = st.columns([1, 5, 1])

with search_area:
    url_col, btn_col = st.columns([5, 1], gap="small")

    with url_col:
        youtube_url = st.text_input(
            "Video URL",
            value=st.session_state.video_url if st.session_state.video_url else "",
            placeholder="Paste YouTube link here...",
            label_visibility="collapsed",
            key="youtube_url_input",
        )

    with btn_col:
        analyze_clicked = st.button(
            "Analyze",
            type="primary",
            use_container_width=True,
            key="analyze_btn",
        )

    # Upload toggle (only before first analysis)
    if not st.session_state.result:
        toggle_label = (
            "🔗 Paste a YouTube link instead"
            if st.session_state.show_upload
            else "📁 Upload a video file instead"
        )
        if st.button(
            toggle_label,
            type="secondary",
            key="toggle_upload_btn",
        ):
            st.session_state.show_upload = not st.session_state.show_upload
            st.rerun()

    # Upload area (shown when toggled)
    uploaded_file = None
    if st.session_state.show_upload:
        uploaded_file = st.file_uploader(
            "Upload Video",
            type=["mp4", "mov", "avi", "mkv", "wav", "mp3"],
            label_visibility="collapsed",
        )


# =====================================================
# Sidebar
# =====================================================
with st.sidebar:
    st.markdown("### Settings")

    language = st.selectbox(
        "Language",
        ["english", "hinglish"],
    )

    st.divider()

    st.markdown("### About")
    st.info(
        """
    **VideoAssist**
    - Whisper
    - LangChain
    - RAG
    - Mistral AI
    - Streamlit
    """
    )


# =====================================================
# Run Pipeline
# =====================================================
if analyze_clicked:
    source = None

    if uploaded_file is not None:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp.write(uploaded_file.read())
        source = temp.name
        st.session_state.video_url = ""

    elif youtube_url.strip():
        source = youtube_url.strip()
        st.session_state.video_url = youtube_url.strip()

    else:
        st.warning("Paste a YouTube link or upload a file to get started.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    status.info("📥 Processing input...")
    progress.progress(15)
    time.sleep(0.3)

    status.info("🎤 Transcribing audio...")
    progress.progress(40)
    time.sleep(0.3)

    status.info("🧠 Generating summary...")
    progress.progress(65)
    time.sleep(0.3)

    status.info("📌 Extracting insights...")
    progress.progress(85)

    try:
        result = run_pipeline(source, language)
        progress.progress(100)
        status.success("✅ Analysis complete!")
        st.session_state.result = result
        st.rerun()
    except Exception as e:
        progress.empty()
        status.error(f"❌ Analysis failed: {str(e)}")
        st.session_state.result = None


# =====================================================
# RESULTS
# =====================================================
if st.session_state.result:
    result = st.session_state.result

    # Results header
    st.markdown(
        """
        <div class="results-header">
            <div class="results-title">Analysis Results</div>
            <div class="results-meta">Powered by Whisper · Mistral · LangChain · RAG</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Video Info Card
    video_title = result.get("title", "Untitled Video")
    st.markdown(
        f"""
        <div class="video-info-card">
            <div class="video-info-title">🎬 {video_title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics Row
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            label="Action Items",
            value=len(result["action_items"]) if isinstance(result["action_items"], list) else 1,
        )

    with m2:
        st.metric(
            label="Key Decisions",
            value=len(result["key_decisions"]) if isinstance(result["key_decisions"], list) else 1,
        )

    with m3:
        st.metric(
            label="Questions",
            value=len(result["open_questions"]) if isinstance(result["open_questions"], list) else 1,
        )

    # Tabs
    tabs = st.tabs(["📝 Summary", "📄 Transcript", "📌 Insights", "💬 Chat"])

    # ── Tab 1: Summary ──
    with tabs[0]:
        st.markdown("### AI Summary")
        st.write(result["summary"])
        st.download_button(
            "⬇ Download Summary",
            result["summary"],
            "summary.txt",
            use_container_width=True,
        )

    # ── Tab 2: Transcript ──
    with tabs[1]:
        st.markdown("### Transcript")
        search_query = st.text_input(
            "🔍 Search transcript",
            placeholder="Type to search...",
            label_visibility="collapsed",
        )
        if search_query:
            lines = result["transcript"].split("\n")
            matching_lines = [
                line for line in lines if search_query.lower() in line.lower()
            ]
            displayed_text = (
                "\n".join(matching_lines) if matching_lines else "No matches found."
            )
        else:
            displayed_text = result["transcript"]

        st.text_area(
            "",
            value=displayed_text,
            height=400,
            label_visibility="collapsed",
        )
        st.download_button(
            "⬇ Download Transcript",
            result["transcript"],
            "transcript.txt",
            use_container_width=True,
        )

    # ── Tab 3: Insights ──
    with tabs[2]:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### ✅ Action Items")
            st.write(result["action_items"])
            st.divider()
            st.markdown("### 🔑 Key Decisions")
            st.write(result["key_decisions"])

        with c2:
            st.markdown("### ❓ Open Questions")
            st.write(result["open_questions"])

    # ── Tab 4: Chat ──
    with tabs[3]:
        st.markdown("### 💬 Chat with Video")

        for role, message in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(message)

        prompt = st.chat_input("Ask anything about the video...")

        if prompt:
            st.session_state.chat_history.append(("user", prompt))

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_question(result["rag_chain"], prompt)
                st.markdown(answer)

            st.session_state.chat_history.append(("assistant", answer))

    # ── Analyze Another ──
    st.divider()
    if st.button("📁 Analyze Another Video", use_container_width=True):
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.video_url = ""
        st.session_state.show_upload = False
        st.rerun()


# =====================================================
# Footer
# =====================================================
st.markdown(
    """
    <div class="footer">
        <p>Powered by Whisper · LangChain · Mistral · Streamlit · RAG</p>
        <p>
            <a href="https://github.com/master-priyansh/F--AI-VIDEO-AGENT" target="_blank">GitHub</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
