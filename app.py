import os
import time
import tempfile

import streamlit as st
import requests

# -------------------------
# Your AI Pipeline
# -------------------------
from main import run_pipeline
from core.rag_engine import ask_question

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Load CSS
# -------------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# -------------------------
# Session State
# -------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.markdown("# ⚙ AI Settings")

    language = st.selectbox(
        "Language",
        ["english", "hinglish"],
    )

    st.divider()

    st.markdown("### About")

    st.info(
        """
AI Meeting Assistant

✔ Whisper

✔ LangChain

✔ RAG

✔ Mistral

✔ Streamlit
"""
    )


# =====================================================
# Hero Section
# =====================================================

col1, col2 = st.columns([3, 2])

with col1:

    st.markdown(
        """
# 🎥 AI Video Assistant

### Transcribe • Summarize • Extract Insights • Chat with Videos
"""
    )



# =====================================================
# Upload Section
# =====================================================

left, right = st.columns(2)

with left:

    uploaded_file = st.file_uploader(
        "Upload Video",
        type=["mp4", "mov", "avi", "mkv", "wav", "mp3"],
    )

with right:

    youtube_url = st.text_input(
        "Or Paste YouTube URL"
    )

st.markdown("")

analyze = st.button(
    "✨ Analyze Video",
    use_container_width=True,
)

# =====================================================
# Run Pipeline
# =====================================================

if analyze:

    source = None

    if uploaded_file:

        temp = tempfile.NamedTemporaryFile(delete=False)

        temp.write(uploaded_file.read())

        source = temp.name

    elif youtube_url:

        source = youtube_url

    else:

        st.warning("Upload a file or enter a YouTube URL.")

        st.stop()

    progress = st.progress(0)

    status = st.empty()

    status.info("🎥 Processing input...")
    progress.progress(15)

    time.sleep(0.5)

    status.info("🎤 Transcribing...")
    progress.progress(40)

    time.sleep(0.5)

    status.info("🧠 Summarizing...")
    progress.progress(65)

    time.sleep(0.5)

    status.info("📌 Extracting insights...")
    progress.progress(85)

    result = run_pipeline(source, language)

    progress.progress(100)

    status.success("Completed!")

    st.session_state.result = result


# =====================================================
# Results
# =====================================================

if st.session_state.result:

    result = st.session_state.result

    st.markdown("---")

    st.success("Analysis Complete")

    # ------------------------
    # Metrics
    # ------------------------

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Action Items",
            len(result["action_items"])
            if isinstance(result["action_items"], list)
            else 1,
        )

    with m2:
        st.metric(
            "Decisions",
            len(result["key_decisions"])
            if isinstance(result["key_decisions"], list)
            else 1,
        )

    with m3:
        st.metric(
            "Questions",
            len(result["open_questions"])
            if isinstance(result["open_questions"], list)
            else 1,
        )

    st.markdown("")

    st.markdown(f"## 📌 {result['title']}")

    tabs = st.tabs(
        [
            "📝 Summary",
            "📄 Transcript",
            "📌 Insights",
            "💬 AI Chat",
        ]
    )

    # =================================================
    # SUMMARY
    # =================================================

    with tabs[0]:

        st.markdown("### AI Summary")

        st.write(result["summary"])

        st.download_button(
            "⬇ Download Summary",
            result["summary"],
            "summary.txt",
        )

    # =================================================
    # TRANSCRIPT
    # =================================================

    with tabs[1]:

        st.markdown("### Transcript")

        st.text_area(
            "",
            result["transcript"],
            height=500,
        )

    # =================================================
    # INSIGHTS
    # =================================================

    with tabs[2]:

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("## ✅ Action Items")

            st.write(result["action_items"])

            st.markdown("---")

            st.markdown("## 🔑 Key Decisions")

            st.write(result["key_decisions"])

        with c2:

            st.markdown("## ❓ Open Questions")

            st.write(result["open_questions"])

    # =================================================
    # CHAT
    # =================================================

    with tabs[3]:

        st.markdown("## Chat with your Video")

        for role, message in st.session_state.chat_history:

            with st.chat_message(role):
                st.markdown(message)

        prompt = st.chat_input("Ask anything...")

        if prompt:

            st.session_state.chat_history.append(
                ("user", prompt)
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    answer = ask_question(
                        result["rag_chain"],
                        prompt,
                    )

                    st.markdown(answer)

            st.session_state.chat_history.append(
                ("assistant", answer)
            )


# =====================================================
# Footer
# =====================================================

st.markdown("---")

st.caption(
    "🚀 Powered by LangChain • Whisper • Mistral • Streamlit • RAG"
)