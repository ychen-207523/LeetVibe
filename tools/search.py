import os
from langchain_core.tools import tool
from tavily import TavilyClient

# Initialize the Tavily Client using the key from your .env file
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


@tool
def search_leetcode_problem(topic: str) -> str:
    """
    Searches for a popular LeetCode problem description based on a specific topic.
    Useful when the user asks for a new problem to solve.

    Args:
        topic (str): The category of the problem (e.g., "Arrays", "Dynamic Programming").

    Returns:
        str: A summary of a relevant LeetCode problem found online.
    """
    query = f"popular leetcode problem interview question {topic} description example"

    response = tavily_client.search(query, max_results=1, include_answer=True)

    # Parsing the result to make it clean for the Agent
    if response and 'results' in response:
        result = response['results'][0]
        title = result.get('title', 'Unknown Problem')
        content = result.get('content', 'No description found.')
        return f"Found Problem: {title}\n\nDescription:\n{content}"

    return "Could not find a problem for that topic."