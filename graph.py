from langgraph.graph import StateGraph, END
from state import AgentState
from agents.manager import manager_node
from agents.interviewer import interviewer_node
from agents.grader import grader_node


# 1. Define the Routing Logic
# This function looks at the "Blackboard" and decides where to go next.
def route_signal(state: AgentState):
    # 1. Analyze the User's input
    messages = state.get("messages", [])
    if messages:
        last_msg = messages[-1].content.lower()

        # FIX: Explicitly check if user wants a NEW problem
        if "give me" in last_msg or "new question" in last_msg or "another" in last_msg or "random" in last_msg:
            return "manager"

        # Check for Java Code
        if "class solution" in last_msg or "public class" in last_msg:
            state["user_code"] = messages[-1].content
            return "grader"

    # 2. Standard Check: If we simply don't have a problem yet, get one.
    if not state.get("problem_description"):
        return "manager"

    # Default: Chat
    return "interviewer"


# 2. Initialize the Graph
workflow = StateGraph(AgentState)

# 3. Add the Nodes (The Agents)
workflow.add_node("manager", manager_node)
workflow.add_node("interviewer", interviewer_node)
workflow.add_node("grader", grader_node)

# 4. Define the Edges (The Wiring)

# START -> Decides where to go based on route_signal
workflow.set_conditional_entry_point(
    route_signal,
    {
        "manager": "manager",
        "grader": "grader",
        "interviewer": "interviewer"
    }
)

# Manager -> Interviewer
# (Once a problem is found, immediately introduce it)
workflow.add_edge("manager", "interviewer")

# Grader -> Interviewer
# (Once code is graded, let the Interviewer explain the result)
workflow.add_edge("grader", "interviewer")

# Interviewer -> END
# (Once the bot speaks, it stops and waits for User Input)
workflow.add_edge("interviewer", END)

# 5. Compile the Application
app = workflow.compile()