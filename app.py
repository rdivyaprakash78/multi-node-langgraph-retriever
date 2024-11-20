from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, START, END, StateGraph
from langchain.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
import streamlit as st
from langchain_experimental.utilities import PythonREPL
from prompts import prompts
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("COHERE_API_KEY")

llm = ChatCohere(cohere_api_key=key)

def wiki_node(state):
    print("inside wiki")
    wiki = WikipediaAPIWrapper()
    user_chat = state["messages"][-1].content
    wiki_result = wiki.run(user_chat) 
    prompt_template = PromptTemplate.from_template(prompts["wiki answer retriever prompt"])
    prompt = prompt_template.invoke({"user_query": user_chat, "wiki_result" : wiki_result})
    response = llm.invoke(prompt)
    return {"messages" : response}

def time_node(state):
    print("inside time")
    python_tool = PythonREPL()
    user_chat = state["messages"][-1].content
    prompt_template = PromptTemplate.from_template(prompts["python code execution prompt"])
    prompt = prompt_template.invoke({"user_input": user_chat})
    response = llm.invoke(prompt)
    print("code : ", response.content)
    py_response = python_tool.run(response.content)
    print(py_response)    
    prompt_template = PromptTemplate.from_template(prompts["python result interpreter prompt"])
    prompt = prompt_template.invoke({"user_input": user_chat, "pyhton_result": py_response})
    response = llm.invoke(prompt)
    return {"messages" : response}

def chatbot(state):
    print("inside chatbot")
    return {"messages" : llm.invoke(state["messages"][-1].content)}

def decision_maker(state):
    user_chat = state["messages"][-1].content
    prompt_template = PromptTemplate.from_template(prompts["decision maker prompt"] )
    prompt = prompt_template.invoke({"user_input": user_chat})
    response = llm.invoke(prompt)
    print("decision :", response.content)
    if response.content == "wikipedia":
        return "wikipedia"
    elif response.content == "time":
        return "time"
    else:
        return "chatbot"

graph = StateGraph(MessagesState)

graph.add_node("wikipedia", wiki_node)
graph.add_node("chatbot",chatbot)
graph.add_node("time", time_node)


graph.add_conditional_edges(START, decision_maker)
graph.add_edge("time", END)
graph.add_edge("chatbot", END)
graph.add_edge("wikipedia", END)

compiled_graph = graph.compile()

st.title("Multi node retrieval application")

user_input = st.text_input("Ask me anything")

if user_input:
    user_text = [HumanMessage(content=user_input)]
    messages = compiled_graph.invoke({"messages": user_text})
    st.write(messages["messages"][-1].content)

    


