import sys
import os
import streamlit as st

# Allow imports from utils folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.document_processing import extract_from_pdf, extract_from_excel
from utils.ollama_integration import ask_ollama


# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Financial Document Q&A Assistant",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Financial Document Q&A Assistant")
st.caption("Upload a financial PDF or Excel document and ask questions about it.")


# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a PDF or Excel file",
    type=["pdf", "xlsx", "xls"]
)

context = ""

if uploaded_file:
    filetype = uploaded_file.name.split(".")[-1].lower()

    with st.spinner("Processing document..."):
        if filetype == "pdf":
            context = extract_from_pdf(uploaded_file)
        elif filetype in ["xlsx", "xls"]:
            context = extract_from_excel(uploaded_file)
        else:
            st.error("Unsupported file format.")

    if context.startswith("ERROR"):
        st.error(context)
        context = ""
    else:
        st.success("✅ Document processed successfully!")


# -----------------------------
# Q&A Section
# -----------------------------
if context:
    st.divider()
    st.subheader("💬 Ask a financial question")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous chats
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['question']}")
        st.markdown(f"**Assistant:** {chat['answer']}")

    question = st.text_input("Ask your question:")

    if question:
        with st.spinner("Thinking..."):
            try:
                answer = ask_ollama(question, context)
            except Exception as e:
                answer = f"Error communicating with Ollama: {e}"

        st.session_state.chat_history.append(
            {"question": question, "answer": answer}
        )

        st.markdown(f"**User:** {question}")
        st.markdown(f"**Assistant:** {answer}")

else:
    st.info("👆 Upload a document to start.")