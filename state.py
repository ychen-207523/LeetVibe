from typing import TypedDict, List, Annotated
import operator
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    The state of the agent graph.
    This is the 'memory' passed between the Router, Interviewer, and Grader.
    """

    messages: Annotated[List[BaseMessage], operator.add]

    sender: str

    # These fields hold the specific data about the coding problem.
    current_topic: str  # e.g., "Arrays", "DP"
    problem_title: str  # e.g., "Two Sum"
    problem_description: str  # The text of the question

    # Used when the user submits code for review
    user_code: str  # The Java code extracted from the chat
    feedback: str  # The analysis from the Grader agent
