<div align="center">

# 🌐 Website Q&A Bot

### ⚡ Powered by RAG + Groq + LangChain

Paste any website URL → Ask questions → 
Get AI-powered answers with source citations!

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-v1.0-green?logo=chainlink)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3--70B-orange?logo=meta)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## ❓ Problem

LLMs like GPT-4 and LLaMA are powerful, but:
- ❌ Can't access live website content
- ❌ Hallucinate when they don't know
- ❌ Have knowledge cutoff dates
- ❌ Can't scrape and analyze web pages

## ✅ Solution

A **RAG-powered Website Q&A Bot** that:
- 🌐 Scrapes any public website in real-time
- 🔍 Searches website content semantically
- 📌 Provides source URL citations
- 🚫 Prevents hallucinations
- ⚡ Ultra-fast with Groq LLM

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌐 **Any URL** | Paste any public website URL |
| 🔍 **Smart Scraping** | Single page or full site crawl |
| 💬 **Natural Language Q&A** | Ask questions in plain English |
| 📌 **Source Citations** | Clickable source URLs for every answer |
| ⚡ **Ultra-Fast** | Groq LLaMA 3.3-70B in < 2 seconds |
| 🗄️ **Persistent Storage** | ChromaDB saves vectors to disk |
| 🧹 **Clean HTML** | Removes nav, footer, scripts automatically |
| 🆓 **100% Free** | Groq free tier + HuggingFace embeddings |

---

## 🏗️ Architecture

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Core language |
| **LangChain v1** | RAG framework |
| **Groq** (LLaMA 3.3-70B) | LLM inference |
| **ChromaDB** | Vector database |
| **HuggingFace** (MiniLM-L6-v2) | Embeddings |
| **BeautifulSoup** | HTML parsing |
| **Streamlit** | Web UI |

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- Groq API Key ([Free](https://console.groq.com))
- HuggingFace Token ([Free](https://huggingface.co/settings/tokens))

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/website-qa-bot.git
cd website-qa-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run application
streamlit run app.py
