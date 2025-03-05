import os
import sys
import asyncio
import nest_asyncio
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message as st_message

# own classes
from scrap.scrapper import WebScrapper
from rag.summarization import WebSummarizer
from rag.ingest import EmbeddingIngestor
from rag.chatbot import ChatBot

# Set Windows event loop policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()
nest_asyncio.apply()

# Session variables
if "url_submitted" not in st.session_state:
    st.session_state.url_submitted = False
if "extraction_done" not in st.session_state:
    st.session_state.extraction_done = False
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "embedding_done" not in st.session_state:
    st.session_state.embedding_done = False
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "summary" not in st.session_state:
    st.session_state.summary = ""

# ---------------------------
# Page Config in streamlit
# ---------------------------

st.set_page_config(layout="wide", page_title="Web-ChatBot")
st.title("Project Chatbot with LLM + RAG")

# ---------------------------
# Streamlit UI
# ---------------------------

page = st.sidebar.selectbox("Menu", ["Home", "AI Chatbot"])

if page == "Home":
    st.markdown(
        """
        ## Welcome to Web-Chatbot
        **Web-Chatbot** is a small chatbot empowered by integration of LLM with RAG of website knowledge extraction through LangChain.
        
        **Functionalities:**
        - **Web Scraping:** Crawl and extract web page content.
        - **Web Summarization:** Generate detailed summaries of the extracted content.
        - **Create Embeddings:** Embeddings with FAISS for vector representation and retrieval of web-scraped information
        - **Chatbot Interface:** Execute Question-Answering task via a conversational agent.

        **Technologies:**
        - **LLM:** Model deepseek-r1:1.5b
        - **FAISS:** vector database to store embeddings
        - **LangChain:** framework to integrate LLM, external data and tools
        - **Streamlit:** python library to fast prototype web apps
        
        Get started!
        """
    )    

elif page == "AI Chatbot":
    with st.form("url_form"):
        url_input = st.text_input("Enter a URL to crawl:")
        submit_url = st.form_submit_button("Submit URL")

        if submit_url and url_input:
            st.session_state.url_submitted = True
            st.session_state.extraction_done = False
            st.session_state.embedding_done = False
            st.session_state.chat_history = []
            st.session_state.summary = ""
    
    if st.session_state.url_submitted:
        col1, col2 = st.columns(2)

        with col1:
            st.header("1. Web-Scrapping")

            if not st.session_state.extraction_done:
                with st.spinner("Extracting website..."):
                    scraper = WebScrapper()
                    extracted = asyncio.run(scraper.crawl(url_input))
                    st.session_state.extracted_text = extracted
                    st.session_state.extraction_done = True
                st.success("Extraction complete!")

            preview = "\n".join([line for line in st.session_state.extracted_text.splitlines() if line.strip()][:5])
            st.text_area("Extracted Text Preview", preview, height=150)

            st.download_button(
                label="Download Extracted Text",
                data=st.session_state.extracted_text,
                file_name="extract_text.txt",
                mime="text/plain",
            )

            st.markdown("---")

            st.header("2. Web-Summarization")

            if st.button("Summarize Web Page", key="summarize_button"):
                with st.spinner("Summarizing..."):
                    summarizer = WebSummarizer()
                    st.session_state.summary = summarizer.summarize(st.session_state.extracted_text)
                st.success("Summarization complete!")

            if st.session_state.summary:
                st.subheader("Summarized Output")
                st.markdown(st.session_state.summary, unsafe_allow_html=False)

        with col2:
            st.header("3. Create Embeddings")

            if st.session_state.extraction_done and not st.session_state.embedding_done:
                if st.button("Create Embeddings"):
                    with st.spinner("Creating embeddings..."):
                        embeddings = EmbeddingIngestor()
                        st.session_state.vectorstore = embeddings.create_embeddings(st.session_state.extracted_text)
                        st.session_state.embedding_done = True
                    st.success("Vectors are created!")

            elif st.session_state.embedding_done:
                st.info("Embeddings have been created.")

            st.markdown("---")

            st.header("4. ChatBot")

            if st.session_state.embedding_done:
                chatbot = ChatBot(st.session_state.vectorstore)
                user_input = st.text_input("Your Message:", key="chat_input")

                if st.button("Send", key="send_button") and user_input:
                    bot_answer = chatbot.qa(user_input)
                    st.session_state.chat_history.append({"user": user_input, "bot": bot_answer})

                    chat_file_content = "\n\n".join([f"User: {chat['user']}\nBot: {chat['bot']}" for chat in st.session_state.chat_history])
                    with open("history/chat_history.txt", "w", encoding="utf-8") as cf:
                        cf.write(chat_file_content)

                if st.session_state.chat_history:
                    for chat in st.session_state.chat_history:
                        st_message(chat["user"], is_user=True)
                        st_message(chat["bot"], is_user=False)
            else:
                st.info("Please create embeddings to activate the chat.")
