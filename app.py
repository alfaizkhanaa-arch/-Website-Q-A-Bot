# app.py
import streamlit as st
import shutil
import os
from rag_pipeline import (
    load_website, split_documents,
    create_vectorstore, build_rag_chain,
    ask_question
)

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="🌐 Website Q&A Bot",
    layout="wide",
    page_icon="🌐"
)

st.title("🌐 Website Q&A Bot ⚡ Powered by Groq")
st.markdown(
    "Paste any **website URL** and ask questions "
    "about its content!"
)

# ── Initialize Session State ──────────────────────────────
if "messages"      not in st.session_state:
    st.session_state.messages      = []
if "chain"         not in st.session_state:
    st.session_state.chain         = None
if "loaded_urls"   not in st.session_state:
    st.session_state.loaded_urls   = []
if "total_chunks"  not in st.session_state:
    st.session_state.total_chunks  = 0

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    # Model selector
    model = st.selectbox(
        "🤖 Groq Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ]
    )

    # Scrape mode
    scrape_mode = st.radio(
        "🔍 Scrape Mode",
        ["single", "full"],
        captions=[
            "Single page only (Fast)",
            "Crawl entire website (Slow)"
        ]
    )

    st.divider()

    # ── URL Input ─────────────────────────────────────────
    st.header("🌐 Add Website URL")

    url_input = st.text_input(
        "Paste a URL:",
        placeholder="https://example.com"
    )

    if st.button("🔍 Load Website", type="primary"):
        if url_input:
            # Basic URL validation
            if not url_input.startswith("http"):
                st.error("❌ Please enter a valid URL "
                         "(starting with http/https)")
            elif url_input in st.session_state.loaded_urls:
                st.warning("⚠️ This URL is already loaded!")
            else:
                with st.spinner(
                    f"🌐 Scraping {url_input}..."
                ):
                    try:
                        # Load + process website
                        docs   = load_website(
                            url_input, mode=scrape_mode
                        )
                        chunks = split_documents(docs)

                        # Build or update vector store
                        vs    = create_vectorstore(chunks)
                        chain = build_rag_chain(vs, model)

                        # Save to session state
                        st.session_state.chain = chain
                        st.session_state.loaded_urls.append(
                            url_input
                        )
                        st.session_state.total_chunks += (
                            len(chunks)
                        )

                        st.success(
                            f"✅ Loaded! ({len(chunks)} chunks)"
                        )

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a URL first!")

    # ── Show Loaded URLs ──────────────────────────────────
    if st.session_state.loaded_urls:
        st.divider()
        st.subheader("📋 Loaded Websites")

        for i, url in enumerate(
            st.session_state.loaded_urls, 1
        ):
            # Truncate long URLs for display
            display_url = (url[:40] + "...")  \
                          if len(url) > 40 else url
            st.write(f"{i}. 🌐 {display_url}")

        st.info(
            f"📊 Total chunks: "
            f"{st.session_state.total_chunks}"
        )

        # ── Clear All Button ──────────────────────────────
        if st.button("🗑️ Clear All", type="secondary"):
            if os.path.exists("./chroma_db"):
                shutil.rmtree("./chroma_db")
            st.session_state.chain        = None
            st.session_state.loaded_urls  = []
            st.session_state.total_chunks = 0
            st.session_state.messages     = []
            st.rerun()

    # ── Quick Load Examples ───────────────────────────────
    st.divider()
    st.subheader("⚡ Quick Load Examples")

    example_urls = {
        "🐍 Python Docs":
            "https://docs.python.org/3/tutorial/index.html",
        "🦜 LangChain Docs":
            "https://python.langchain.com/docs/introduction",
        "📊 Wikipedia - AI":
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
    }

    for label, url in example_urls.items():
        if st.button(label):
            st.session_state["prefill_url"] = url
            st.rerun()

# ── Main Chat Interface ───────────────────────────────────

# Show status
if st.session_state.loaded_urls:
    st.success(
        f"✅ {len(st.session_state.loaded_urls)} "
        f"website(s) loaded — Ready to answer!"
    )
else:
    st.info("👈 Add a website URL in the sidebar to begin!")

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if question := st.chat_input(
    "💬 Ask anything about the website..."
):
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user"):
        st.markdown(question)

    if st.session_state.chain:
        with st.chat_message("assistant"):
            with st.spinner("⚡ Searching website..."):
                result  = ask_question(
                    st.session_state.chain,
                    question
                )
                answer  = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                # ✅ Show clickable source URLs
                if sources:
                    with st.expander("🔗 Sources"):
                        for source in sources:
                            st.markdown(f"- [{source}]({source})")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
    else:
        st.warning(
            "⚠️ Please load a website first "
            "from the sidebar!"
        )