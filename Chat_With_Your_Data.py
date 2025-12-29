import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    create_pandas_dataframe_agent,
)
from langchain_core.messages import HumanMessage, AIMessage

from src.models.llm import load_llm
from src.agents.action import classify_intent, planner, executor
from src.ui.chat_history import display_chat_history
from src.agents.load_data import load_data
from src.agents.summary import summary
from src.types.state_types import chatState

from langgraph.graph import StateGraph, START

# =========================
# ENV + LLM
# =========================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash"
llm = load_llm(MODEL_NAME, api_key)

# =========================
# INITIAL STATE TEMPLATE
# =========================
state: chatState = {
    "query": "",
    "df": None,
    "dataset_context": "",
    "llm": llm,
    "agent": None,
    "intent": "",
    "executed_code": None,
    "fig": None,
    "data_table": None,
    "response": None,
}


# =========================
# LANGGRAPH NODES
# =========================
def input_node(state: chatState):
    return {"messages": [HumanMessage(content=state["query"])]}


def intent_node(state: chatState):
    return classify_intent(state)


def edge_to_planner(state):
    return state["intent"] == "PLANNER"


def edge_to_executor(state):
    return state["intent"] != "PLANNER"


def planner_node(state: chatState):
    result = planner(state)
    return result


def executor_node(state: chatState):
    result = executor(state)
    return result


# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(page_title="Chat with your data", layout="wide")
st.header("Chat with Your Data using LLMs")

# =========================
# STREAMLIT SESSION INIT
# =========================
if "df" not in st.session_state:
    st.session_state.df = None

if "agent" not in st.session_state:
    st.session_state.agent = None

if "dataset_context" not in st.session_state:
    st.session_state.dataset_context = ""

if "history" not in st.session_state:
    st.session_state.history = []
# =========================
# SIDEBAR – LOAD DATA
# =========================
with st.sidebar:
    # upload CSV
    uploaded_file = st.file_uploader("Up your file csv here", type="csv")
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        state["df"] = st.session_state.df

    # upload text
    st.markdown("Load text context (optional)")
    text_source_type = st.selectbox(
        "Select text source",
        options=["none", "pdf", "docx", "txt"],
    )
    text_file = None
    if text_source_type in ["pdf", "docx", "txt"]:
        text_file = st.file_uploader(
            "Upload file text",
            type=[text_source_type],
            key="text_file",
        )

    # load text
    if st.button("Load data"):
        documents = None

        if text_source_type in ["pdf", "docx", "txt"] and text_file:
            file_path = f"temp.{text_source_type}"
            with open(file_path, "wb") as f:
                f.write(text_file.read())

            documents = load_data(text_source_type, file_path)

        if documents:
            full_text = " ".join([doc.page_content for doc in documents])
            st.session_state.dataset_context = summary(full_text, state["llm"])
            state["dataset_context"] = st.session_state.dataset_context
            st.write(state["dataset_context"])

# =========================
# SHOW DATASET
# =========================
if st.session_state.df is not None:
    st.write("Your Dataset ", st.session_state.df.head())

# =========================
# CREATE AGENT
# =========================
if st.session_state.df is not None and st.session_state.agent is None:
    st.session_state.agent = create_pandas_dataframe_agent(
        llm=state["llm"],
        df=st.session_state.df,
        agent_type="tool-calling",
        allow_dangerous_code=True,
        verbose=True,
        return_intermediate_steps=True,
    )
state["agent"] = st.session_state.agent

# =========================
# USER INPUT
# =========================
query = st.text_input("Enter your question: ")
if query:
    state["query"] = query

# =========================
# BUILD LANGGRAPH
# =========================


@st.cache_resource
def build_graph():
    graph = StateGraph(state_schema=chatState)

    graph.add_node("input", input_node)
    graph.add_node("intent", intent_node)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)

    graph.add_edge(START, "input")
    graph.add_edge("input", "intent")

    graph.add_conditional_edges(
        "intent",
        lambda state: "planner" if state["intent"] == "PLANNER" else "executor",
        {
            "planner": "planner",
            "executor": "executor",
        },
    )

    return graph.compile()


app = build_graph()

final_state = None

if query and state["agent"] is not None:
    run_state = state.copy()
    final_state = app.invoke(run_state)
    if final_state:
        st.write(final_state["response"])
    if isinstance(final_state.get("data_table"), (pd.DataFrame, pd.Series)):
        st.dataframe(final_state["data_table"])
    if final_state.get("fig"):
        st.pyplot(final_state["fig"])
    if final_state.get("executed_code"):
        st.code(final_state["executed_code"], language="python")


# =========================
# SAVE CHAT HISTORY
# =========================
if final_state and (
    len(st.session_state.history) == 0
    or st.session_state.history[-1]["content"] != final_state["response"]
):
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.history.append(
        {
            "role": "assistant",
            "content": final_state["response"],
            "data_table": final_state.get("data_table"),
            "fig": final_state.get("fig"),
            "code": final_state.get("executed_code"),
        }
    )


# =========================
# DISPLAY CHAT HISTORY
# =========================
display_chat_history(st.session_state.history)
