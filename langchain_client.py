from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    print("Hello World!")

if __name__ == "__main__":
    asyncio.run(main())
