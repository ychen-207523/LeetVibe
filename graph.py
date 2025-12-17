from langgraph.graph import StateGraph, END
from state import AgentState
from agents.manager import manager_node
from agents.interviewer import interviewer_node
from agents.grader import grader_node


# 1. Define the Routing Logic
# This function looks at the "Blackboard" and decides where to go next.
def route_signal(state: AgentState):
    # Check 1: Do we have a problem?
    if not state.get("problem_description"):
        return "manager"

    # Check 2: Look at the LAST message (The User's input)
    messages = state.get("messages", [])
    if messages:
        last_msg = messages[-1].content.lower()

        # Simple heuristic: If it looks like Java, send to Grader
        if "class solution" in last_msg or "public class" in last_msg:
            # We also save the code to the state here for the Grader to find easily
            state["user_code"] = messages[-1].content
            return "grader"

    # Default: Send to the conversationalist
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