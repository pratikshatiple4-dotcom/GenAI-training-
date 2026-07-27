# import os 
# # from langchain_community.llms import Ollama
# from langchain_ollama import OllamaLLM

# import streamlit as st 
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM 


#prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the question asked"),
        ("user","Question:{question}")
    ]
)

# streamlit template
st.title("Langchain demo with Gemma model")
input_text=st.text_input("What question you have in mind?")

# ollama model
# llm=Ollama(model="gemma2:2b")
llm = OllamaLLM(model="gemma2:2b")

output_parser=StrOutputParser()
chain=prompt|llm|output_parser

st.write(chain.invoke({"question":input_text}))