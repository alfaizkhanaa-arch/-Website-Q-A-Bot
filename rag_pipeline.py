import  os
from langchain_community.document_loaders import WebBaseLoader,RecursiveUrlLoader
from langchain_classic.chains import  RetrievalQA
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from langchain_huggingface import  HuggingFaceEmbeddings
from langchain_chroma import  Chroma
from langchain_groq import  ChatGroq
from langchain_core.prompts import  PromptTemplate
from bs4 import  BeautifulSoup,SoupStrainer
from dotenv import  load_dotenv


load_dotenv()


### Emebedding 

embeddings = HuggingFaceEmbeddings()




# ── Clean HTML ─────────────────────────────────────────────
def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["nav", "footer", "script",
                     "style", "header", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

# ── Load Website ───────────────────────────────────────────
def load_website(url: str, mode: str = "single"):
    print(f"🌐 Loading {url}")

    if mode == "single":
        loader = WebBaseLoader(
            web_paths=[url],
            bs_kwargs={
                "parse_only": SoupStrainer(   
                    ["p", "h1", "h2", "h3",
                     "article", "section", "main"]
                )
            }
        )
    else:
        loader = RecursiveUrlLoader(
            url=url,
            max_depth=2,
            extractor=clean_html
        )

    documents = loader.load()

    for doc in documents:
        doc.metadata["source_url"] = url

    print(f"✅ Loaded {len(documents)} page(s)")
    return documents
### Split Documents 
def split_documents(documents) :
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100,
        separators = ["\n\n", "\n", ".", " "]

     )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split {len(chunks)} chunks")
    return chunks

# ── Create Vector Store ───────────────────────────────────
def create_vectorstore(chunks,persist_dir = './chroma_db'):
    vectorstore = Chroma.from_documents(
        documents=  chunks,
        embedding =  embeddings,
        persist_directory =  persist_dir
    )
    print("✅ Chorma db Created!")
    return vectorstore
  
### prompt
prompt_template = """
You are the helpful assistant that answer questions based only on the provided website content.

Rules:
-Use ONLY the context below for answer
-if the answer is not found say:
"I couldn't find this information on the website."
-Mention the sourse of URL when possible
-Be concise and precise

Conext : 
{context}

Question : {question}
Answer :
"""
PROMPT =  PromptTemplate(
    template = prompt_template,
    input_variables = ["context", "question"]
)

### Build RAG Chain
def build_rag_chain(vectorstore,model="llama-3.3-70b-versatile"):
    llm = ChatGroq (
        model= model,
        temperature=0.2,
        groq_api_key = os.getenv("GROQ_API_KEY")
    )
    retriever =  vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs= {"k" : 4}
    )
    qa_chain =  RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = 'stuff',
        retriever =  retriever,
        return_source_documents = True,
        chain_type_kwargs ={'prompt' : PROMPT}
    )
    print("✅ Website RAG Chain Ready!")
    return qa_chain
 # ── Ask Question  
def ask_question(qa_chain,question:str):
    result =  qa_chain.invoke({"query" :question})
    answer = result["result"]
    src_docs =  result['source_documents'] 
    if not src_docs:
        return {
            "answer": "❌ No relevant info found.",
            "sources": []
        } 
    # ✅ Show source URLs
    sources = list(set([
        doc.metadata.get("source", "Unknown URL")
        for doc in src_docs
    ]))

    return {
        "answer":  answer,
        "sources": sources
    }