# Chat with Documents using RAG (Retreival Augment Generation)
# question embedding -> sematic search -> | document | embedding | vector store | -> ranked results -> LLM -> answer

import warnings

from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

warnings.filterwarnings("ignore")

model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv(
    "GOOGLE_API_KEY"), temperature=0.2, convert_system_message_to_human=True)

# https://arxiv.org/pdf/1706.03762.pdf
pdf_loader = PyPDFLoader("test/attention_is_all_you_need.pdf")

pages = pdf_loader.load_and_split()
print("Pages:", len(pages))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000, chunk_overlap=1000)
context = "\n\n".join(str(p.page_content) for p in pages)
texts = text_splitter.split_text(context)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))

vector_index = Chroma.from_texts(
    texts, embeddings).as_retriever(search_kwargs={"k": 5})

qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index,
    return_source_documents=True
)

question = "Describe the Multi-head attention layer in detail?"
response = qa_chain({"query": question})
print("Answer1:", response['result'])

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""

# Run chain
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index,
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

question = "Describe the Multi-head attention layer in detail?"
response = qa_chain({"query": question})
print("\nAnswer2:", response['result'])

question = "Describe Random forest?"
response = qa_chain({"query": question})
print("\nAnswer3:", response['result'])
