import asyncio

from claude_agent_sdk import ClaudeAgentOptions, query
from dotenv import load_dotenv

load_dotenv()

TOPIC = "What are the current trends in AI developer interests and home projects?"


async def main():
    print(f"Researching: {TOPIC}\n")
    async for message in query(
        prompt=f"Research this topic and write a concise summary: {TOPIC}",
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch"],
            permission_mode="bypassPermissions",
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


if __name__ == "__main__":
    asyncio.run(main())
