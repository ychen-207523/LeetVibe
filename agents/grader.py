from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from state import AgentState

# 1. Initialize the LLM
# In a real microservice, this could be a specialized coding model like 'DeepSeek-Coder'
llm = ChatOpenAI(model="gpt-4o")

# 2. The Code Review Prompt
grader_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a Senior Software Engineer conducting a code review.

     Your Goal: Analyze the user's solution for correctness and complexity.

     Current Problem: {problem}

     User's Code:
     {code}

     Output your review in this exact format:
     STATUS: [PASS / FAIL]
     COMPLEXITY: [Time Complexity, e.g., O(n)]
     FEEDBACK: [Brief explanation of bugs or optimization tips]
     """),
])


def grader_node(state: AgentState):
    """
    Analyses the user's code for logical correctness and efficiency.
    """
    # Read from State
    problem = state.get("problem_description")
    code = state.get("user_code", "")

    # Run the Analysis
    chain = grader_prompt | llm
    response = chain.invoke({
        "problem": problem,
        "code": code
    })

    review = response.content

    # Simple logic to determine success
    solved = "STATUS: PASS" in review

    # Format the message for the user
    feedback_msg = f"**Code Review:**\n{review}"

    # Write to State
    return {
        "sender": "Grader",
        "feedback": review,
        "solved_status": solved,
        "messages": [feedback_msg]
    }