"""
Scalix SDK — Example 07: Custom Tools

Create agents with custom Python function tools.
Tools are defined using type hints and docstrings.

Prerequisites:
    pip install scalix
    export ANTHROPIC_API_KEY=your-key
"""

import asyncio
from scalix import Agent, Tool


# --- Define custom tools with @Tool.function ---

@Tool.function
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In production, call a real weather API
    weather_data = {
        "San Francisco": "62°F, Foggy",
        "New York": "45°F, Cloudy",
        "London": "50°F, Rainy",
        "Tokyo": "68°F, Sunny",
    }
    return weather_data.get(city, f"Weather data not available for {city}")


@Tool.function
async def search_docs(query: str) -> str:
    """Search internal documentation for relevant information."""
    # Async tools are supported — call your real search API here
    return f"Found 3 results for '{query}': [Doc A, Doc B, Doc C]"


@Tool.function
def calculate_shipping(weight: float, destination: str) -> str:
    """Calculate shipping cost based on weight and destination."""
    base_rate = 5.99
    rate_per_kg = 2.50
    international_surcharge = 15.00

    cost = base_rate + (weight * rate_per_kg)
    if destination.lower() not in ["us", "usa", "united states"]:
        cost += international_surcharge

    return f"${cost:.2f} for {weight}kg to {destination}"


async def main():
    agent = Agent(
        model="auto",
        instructions=(
            "You are a helpful customer support agent. "
            "Use the available tools to assist customers."
        ),
        tools=[
            get_weather,
            search_docs,
            calculate_shipping,
        ],
    )

    result = await agent.run(
        "I want to ship a 3.5kg package to London. "
        "What's the cost and what's the weather like there?"
    )
    print(result.output)

    print(f"\nTools called: {len(result.tool_calls)}")
    for tc in result.tool_calls:
        print(f"  - {tc.tool_name}({tc.arguments}) → {tc.result}")


if __name__ == "__main__":
    asyncio.run(main())
