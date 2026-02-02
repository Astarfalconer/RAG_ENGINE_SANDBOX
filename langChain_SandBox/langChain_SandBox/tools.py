from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"The weather in {city} is sunny with a high of 75°F."

@dataclass
class Context:
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Get the user's location based on their user ID."""
    # In a real implementation, this would query a database or external service.
    user_id = runtime.context.user_id  

    return f"User {user_id} is located in New York City."                 