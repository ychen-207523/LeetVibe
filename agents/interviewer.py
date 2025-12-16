from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from state import AgentState

# 1. Initialize the Brain (GPT-4o)
llm = ChatOpenAI(model="gpt-4o")

# 2. Define the Persona (The System Prompt)
# Notice {problem} - this is where we inject the data from the Manager.
interviewer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a strict but helpful technical interviewer. 
     The user is solving this problem:
     {problem}

     Rules:
     1. NEVER write the full solution code.
     2. If the user asks for a hint, give a subtle conceptual clue.
     3. If the user shares code, acknowledge it and say you are passing it to the Grader.
     4. Be concise.
     """),
    ("placeholder", "{messages}")
])


def interviewer_node(state: AgentState):
    """
    The Interviewer Agent node.
    It reads the problem from the 'Blackboard' (State) and talks to the user.
    """
    # 1. Get the data from the Blackboard
    # We use .get() to be safe, just like map.getOrDefault() in Java
    current_problem = state.get("problem_description", "No problem selected yet.")
    messages = state.get("messages", [])

    # 2. Prepare the chain (Prompt -> LLM)
    chain = interviewer_prompt | llm

    # 3. Run the "Brain"
    response = chain.invoke({
        "problem": current_problem,
        "messages": messages
    })

    # 4. Return the result to be added to history
    return {
        "sender": "Interviewer",
        "messages": [response]
    }