from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from state import AgentState
from tools.search import search_leetcode_problem

llm = ChatOpenAI(model="gpt-4o")

# This tells the LLM who it is. Notice we give it "Tools".
manager_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Study Manager. Your job is to select a LeetCode problem for the user."),
    ("user", "The user wants to practice topic: {topic}. Find a good problem.")
])


# This is the function LangGraph will call.
def manager_node(state: AgentState):
    """
    The Manager Agent decides which problem to practice.
    """
    topic = state.get('current_topic', 'General')

    # Logic: Search for a problem using the tool we made
    problem_text = search_leetcode_problem(topic)

    # We update the state with the new problem
    return {
        "sender": "Manager",
        "problem_description": problem_text,
        "messages": ["I have found a problem for you. Let me introduce you to the Interviewer."]
    }