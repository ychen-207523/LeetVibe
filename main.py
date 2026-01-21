from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
from graph import app

def main():
    print("🤖 LeetVibe is running! (Type 'quit' to exit)")
    print("---------------------------------------------")

    # 1. Initialize the "Blackboard" (State)
    # We start with an empty history.
    current_state = {
        "messages": [],
        "current_topic": "General",# Default topic
        "problem_description": None,
        "user_code": None,
        "sender": "User"
    }

    while True:
        # 2. Get User Input
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        # 3. Update State
        # We add your message to the history before sending it to the Agent.
        # We must use 'HumanMessage' so the LLM knows who is talking.
        current_state["messages"].append(HumanMessage(content=user_input))
        current_state["sender"] = "User"

        # 4. Run the Agent (The Handoff Magic)
        # app.invoke(state) runs the graph logic we defined in graph.py
        # It passes the baton between Manager -> Interviewer -> Grader
        result = app.invoke(current_state)

        # 5. Update Local State
        # The result contains the NEW history (with the Agent's response added).
        # We save this so the bot remembers context for the next turn.
        current_state = result

        # 6. Print the Response
        # The last message in the list is the Agent's reply.
        last_msg = current_state["messages"][-1]
        print(f"\nAgent: {last_msg.content}\n")
        print("---------------------------------------------")

if __name__ == "__main__":
    main()