import pandas as pd
import matplotlib.pyplot as plt
from typing import TypedDict, List
from langchain_core.messages import BaseMessage


class chatState(TypedDict):
    query: str
    df: pd.DataFrame
    dataset_context: str
    executed_code: str | None
    fig: plt.Figure | None
    data_table: pd.DataFrame | None
    llm: object
    agent: object | None
    intent: str
    response: str | None
    messages: List[BaseMessage]
