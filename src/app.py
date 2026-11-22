"""Streamlit UI for Shinri (真理) - Mutual Fund Facts Assistant."""
import streamlit as st
from src.config import HDFC_SCHEMES
from src.rag.pipeline import ShinriRAGPipeline

st.set_page_config(
    page_title="Shinri (真理) - MF Facts Assistant",
    page_icon="📈",
    layout="centered"
)

# Custom Groww-inspired CSS styling
st.markdown("""
<style>
    .stApp {
        background-color: #0A0E17;
        color: #FFFFFF;
    }
    .header-box {
        padding: 18px 24px;
        background: #161F30;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }
    .status-pill {
        display: inline-block;
        background: rgba(0, 208, 156, 0.12);
        color: #00D09C;
        border: 1px solid rgba(0, 208, 156, 0.25);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .source-box {
        margin-top: 8px;
        padding: 6px 12px;
        background: rgba(0, 208, 156, 0.08);
        border-left: 3px solid #00D09C;
        border-radius: 4px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <div class="status-pill">● Facts-Only &bull; No Investment Advice</div>
    <h2 style="margin: 0; font-size: 24px; font-weight: 700;">Shinri (真理)</h2>
    <p style="color: #94A3B8; font-size: 13.5px; margin-top: 4px;">
        Verifiable mutual fund information assistant covering 5 HDFC schemes on Groww.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "pipeline" not in st.session_state:
    st.session_state.pipeline = ShinriRAGPipeline()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Prompt Buttons
st.markdown("**Try asking:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("Expense ratio of HDFC Small Cap?"):
        st.session_state.user_query = "What is the expense ratio of HDFC Small Cap Direct Growth?"
    if st.button("Lock-in period for HDFC ELSS?"):
        st.session_state.user_query = "What is the lock-in period for HDFC ELSS Tax Saver?"
with col2:
    if st.button("Exit load for HDFC Large Cap?"):
        st.session_state.user_query = "What is the exit load for HDFC Large Cap Fund?"
    if st.button("How to download capital gains statement?"):
        st.session_state.user_query = "How do I download my capital gains statement on Groww?"

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            st.markdown(f"<div class='source-box'><b>Verified Source:</b> <a href='{msg['sources'][0]}' target='_blank'>{msg['sources'][0]}</a></div>", unsafe_allow_html=True)
        if "chunks" in msg and msg["chunks"]:
            with st.expander(f"Inspect Evidence Chunks ({len(msg['chunks'])})"):
                for idx, c in enumerate(msg["chunks"], 1):
                    meta = c["metadata"]
                    st.caption(f"**Chunk {idx}:** {meta['scheme_name']} ({meta['section']})")
                    st.text(c["text"][:250] + "...")

# Chat Input Handler
user_input = st.chat_input("Ask a question about HDFC mutual fund schemes...")
if "user_query" in st.session_state and st.session_state.user_query:
    user_input = st.session_state.user_query
    st.session_state.user_query = None

if user_input:
    # Append user question
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Retrieving verified scheme disclosures..."):
            result = st.session_state.pipeline.query(user_input)

        st.markdown(result["answer"])
        if result.get("sources"):
            st.markdown(f"<div class='source-box'><b>Verified Source:</b> <a href='{result['sources'][0]}' target='_blank'>{result['sources'][0]}</a></div>", unsafe_allow_html=True)
        if result.get("retrieved_chunks"):
            with st.expander(f"Inspect Evidence Chunks ({len(result['retrieved_chunks'])})"):
                for idx, c in enumerate(result["retrieved_chunks"], 1):
                    meta = c["metadata"]
                    st.caption(f"**Chunk {idx}:** {meta['scheme_name']} ({meta['section']})")
                    st.text(c["text"][:250] + "...")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result.get("sources", []),
        "chunks": result.get("retrieved_chunks", [])
    })

# Footer
st.markdown("---")
st.caption("Facts-only assistance. No personalized investment advice or return projections. Last updated: 27 September 2026.")
