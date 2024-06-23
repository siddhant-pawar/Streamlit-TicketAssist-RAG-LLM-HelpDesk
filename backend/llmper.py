import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv

# Ensure 'pdfs' directory exists or create it
PDFS_DIR = 'pdfs'
os.makedirs(PDFS_DIR, exist_ok=True)

embeddings = SpacyEmbeddings(model_name="en_core_web_sm")
load_dotenv()
#anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to read PDF content
def pdf_read(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create FAISS vector store from text chunks
def vector_store(text_chunks):
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(os.path.join(PDFS_DIR, "faiss_db"))

# Function to interact with chatbot using retrieved documents
def get_conversational_chain(tools, question):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=openai_api_key)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer"""),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    tool = [tools]
    agent = create_tool_calling_agent(llm, tool, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True)
    response = agent_executor.invoke({"input": question})
    return response

# Function to handle user input and initiate conversation
def user_input(user_question):
    new_db = FAISS.load_local(os.path.join(PDFS_DIR, "faiss_db"), embeddings, allow_dangerous_deserialization=True)
    retriever = new_db.as_retriever()
    retrieval_chain = create_retriever_tool(retriever, "pdf_extractor", "This tool is to give answer to queries from the pdf")
    return get_conversational_chain(retrieval_chain, user_question)

# Function to handle PDF upload and processing
def process_pdf_upload(pdf_docs):
    for idx, pdf in enumerate(pdf_docs):
        with open(os.path.join(PDFS_DIR, f"uploaded_file_{idx}.pdf"), "wb") as f:
            f.write(pdf.read())
    
    raw_text = pdf_read(pdf_docs)
    text_chunks = get_chunks(raw_text)
    vector_store(text_chunks)

def show_upload_interface():
    pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            process_pdf_upload(pdf_docs)
            st.success("Done")

def show_chat_interface():
    st.title("Chat with our assistant!!!")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.text_input("Ask a Question from the LLM Bot")
    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)
        try:
            response = user_input(user_question)
            with st.chat_message("assistant"):
                st.write(response['output'])
            st.session_state.messages.append({"role": "assistant", "content": response['output']})
        except Exception as e:
            st.error(f"Error: {e}")
