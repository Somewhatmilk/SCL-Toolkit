#!/usr/bin/env python3

import os
import time
from typing import List, Dict, Any
import streamlit as st
from streamlit_chat import message
from streamlit_extras.add_vertical_space import add_vertical_space
import time
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
# from langchain.llms import GPT4All, LlamaCpp
from constants import CHROMA_SETTINGS
from transformers import AutoModel
# from numpy.linalg import norm
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto", torch_dtype=torch.float16)
# Load environment variables from a .env file
load_dotenv()
token: str = os.getenv("TOKEN")
# emb_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en',token=token, trust_remote_code=True)

def main() -> None:

    st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

    with st.sidebar:
        st.title('🤗💬 Industrial Chatbot')
        st.markdown('''
        ## About

    *Chatbot Terms and Conditions:*

    *Introduction:*
    Welcome to the SCL System Customer Service Chatbot! Before you engage with our chatbot, please take a moment to review and understand the following terms and conditions. Your use of the chatbot implies your agreement to comply with these terms.

    *Capabilities:*
    1. *Informational Assistance:* The chatbot is designed to offer information and assistance related to our products and services.
    2. *Query Resolution:* It can help address common queries, guide you through processes, and provide relevant information.
    3. *Limited Personalization:* The chatbot may use minimal personal information to enhance user experience but does not store or process sensitive data.

    By using our Customer Service Chatbot, you acknowledge that you have read, understood, and agreed to these terms and conditions. If you disagree, please refrain from using the chatbot. For questions or concerns, contact our customer support through official channels.
                    
    *Restrictions:*
    1. *No Legal Advice:* The chatbot does not provide legal advice or opinions. For legal matters, consult a professional.
    2. *Limited Scope:* The chatbot's capabilities are confined to predefined tasks and information related to our products and services.
    3. *No Financial Transactions:* The chatbot does not facilitate or process financial transactions. Please use our official channels for such transactions.

    *Data Usage and Privacy:*
    1. *Data Collection:* The chatbot may collect limited personal information to improve user experience and address queries. This data is handled according to our privacy policy.
    2. *Security Measures:* We employ security measures to safeguard the data collected by the chatbot. However, avoid sharing sensitive personal information.

    *Consent:*
    1. *Express Consent:* Before collecting any sensitive data or using it beyond the chatbot's scope, we will seek your express consent.
    2. *Opt-out Option:* You can opt-out of sharing information or terminate the chat at any time.

    *Liability:*
    1. *No Guarantees:* While the chatbot aims for accuracy, we do not guarantee its completeness or accuracy.
    2. *Limited Liability:* We are not liable for any loss or damage resulting from the use of the chatbot.

    *Termination:*
    We reserve the right to terminate or suspend chatbot services without notice.

    *Updates:*
    These terms and conditions may be updated periodically. Your continued use of the chatbot implies acceptance of the latest version.

    SCL System
    Product Search
    HOME
    PRODUCTS
    ENERGY SOLUTIONS
    CAREERS
    ABOUT US
    CONTACT US
    SCL E-STORE
    > Contact Us
    Contact Us
    SCL System Enterprise Pte Ltd
    41 Jalan Pemimpin,
    #02-01A Kong Beng Industrial Building,
    Singapore 577186

    Phone/WhatsApp: +65-62599968

    Fax: +65-62599282

    Email: sales@sclsystem.com.sg

    Copyright © 2023 SCL SystemTerms & Conditions | Privacy Policy
        ''')
        add_vertical_space(5)
        st.write('hello World')
        


    # Configuration parameters loaded from environment variables
    embeddings_model_name: str = os.getenv("EMBEDDINGS_MODEL_NAME")
    persist_directory: str = os.getenv('PERSIST_DIRECTORY')
    model_type:str = os.getenv('MODEL_TYPE')
    model_path: str = os.getenv('MODEL_PATH')
    model_n_ctx: int = int(os.getenv('MODEL_N_CTX',1024))
    model_n_batch: int = int(os.getenv('MODEL_N_BATCH', 8))
    n_source_chunks = int(os.getenv('TARGET_SOURCE_CHUNKS', 4))
    
          
    # Initialize HuggingFace embeddings model
    embeddings: HuggingFaceEmbeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)


    # Initialize Chroma vector store
    db: Chroma = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    llm_dict = {"tokenizer": tokenizer, "model": model}
    # Create a retriever using Chroma with specified search parameters
    retriever: RetrievalQA = db.as_retriever(search_kwargs={"k": n_source_chunks})
    
    # Initialize an empty list for callbacks (none provided in the original code)
    callbacks: List[StreamingStdOutCallbackHandler] = []
    # if model_type == "t5-small":
    llm : T5ForConditionalGeneration = T5ForConditionalGeneration(model_path=llm_dict, n_ctx=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False)
    # else:
        # raise Exception(f"Model type {model_type} id not supported.")

    # Create a RetrievalQA instance with the specified LLM, chain type, and retriever
    qa: RetrievalQA = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    
    # Interactive questions and answers loop
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    res: Dict[str, Any] = qa("Your Queries")
    docs: List[Any] = res['source_documents']
    
    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    query = st.text_input("Enter a query:")
    with st.spinner('Loading...'):
        time.sleep(5)
        
    if query == "exit":
        st.stop()


    
    for doc in docs:
        st.write("\n> " + doc.metadata["source"] + ":")
        st.write(doc.page_content)
    
    if prompt := st.chat_input("Say something"):
        st.session_state.messages.append({"role": "user", "content": res})
        
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
        outputs = llm.generate(input_ids)
        st.write(tokenizer.decode(outputs[0]))
if __name__ == "__main__":
        main()  


 

    
    
   
