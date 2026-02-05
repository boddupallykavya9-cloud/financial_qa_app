import sys
import os
import streamlit as st

# -------------------------------------------------
# Allow imports from utils folder
# -------------------------------------------------
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.document_processing import extract_from_excel, extract_from_pdf
from utils.ollama_integration import ask_ollama
from utils.answer_router import answer_question


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Financial Document Q&A Assistant",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Financial Document Q&A Assistant")
st.caption("Upload a financial Excel or PDF and chat with it like ChatGPT.")


# -------------------------------------------------
# Session state initialization
# -------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "excel_data" not in st.session_state:
    st.session_state.excel_data = None

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

if "current_file" not in st.session_state:
    st.session_state.current_file = None


# -------------------------------------------------
# File upload
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload an Excel or PDF file",
    type=["xlsx", "xls", "pdf"]
)

if uploaded_file:
    # Process ONLY if a NEW document is uploaded
    if st.session_state.current_file != uploaded_file.name:
        with st.spinner("Processing document..."):
            if uploaded_file.name.lower().endswith(("xlsx", "xls")):
                st.session_state.excel_data = extract_from_excel(uploaded_file)
                st.session_state.pdf_text = None
            else:
                st.session_state.pdf_text = extract_from_pdf(uploaded_file)
                st.session_state.excel_data = None

        # Reset chat ONLY for new document
        st.session_state.chat_history = []
        st.session_state.current_file = uploaded_file.name

        st.success("✅ Document processed successfully!")


# -------------------------------------------------
# Chat UI (ChatGPT-style with bottom search bar)
# -------------------------------------------------
if st.session_state.excel_data or st.session_state.pdf_text:

    st.divider()

    # Display chat history (always visible)
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    # -------------------------------------------------
    # ChatGPT-style search bar (BOTTOM + SEND ARROW)
    # -------------------------------------------------
    user_question = st.chat_input(
        "Ask a financial question…"
    )

    if user_question:
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_question)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = answer_question(
                    question=user_question,
                    excel_data=st.session_state.excel_data,
                    pdf_text=st.session_state.pdf_text,
                    chat_history=st.session_state.chat_history,
                    ask_ollama=ask_ollama
                )
            st.markdown(answer)

        # Save conversation (DO NOT clear)
        st.session_state.chat_history.append({
            "question": user_question,
            "answer": answer
        })

else:
    st.info("👆 Upload a document to start chatting.")