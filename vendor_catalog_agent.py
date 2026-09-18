"""Agent that uses the vendor catalog MCP tool."""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from agents import Agent, Runner, set_default_openai_api, set_default_openai_client
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from dotenv import load_dotenv
from openai import AsyncOpenAI


PROJECT_FOLDER = Path(__file__).resolve().parent
load_dotenv(PROJECT_FOLDER / ".env")


def configure_model_client() -> None:
    """Configure the NRP OpenAI-compatible endpoint used by the course examples."""
    base_url = os.getenv("NRP_BASE_URL")
    api_key = os.getenv("NRP_API_KEY")
    if not base_url or not api_key:
        raise RuntimeError("Set NRP_BASE_URL and NRP_API_KEY in .env before running the agent.")
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    set_default_openai_client(client, use_for_tracing=False)
    set_default_openai_api("chat_completions")


async def ask_agent(question: str) -> str:
    """Run one question through the agent and its MCP server."""
    configure_model_client()
    server_path = PROJECT_FOLDER / "catalog_mcp_server.py"
    async with MCPServerStdio(
        name="Vendor Catalog MCP",
        params=MCPServerStdioParams(
            command=sys.executable,
            args=[str(server_path)],
        ),
        client_session_timeout_seconds=90,
    ) as server:
        agent = Agent(
            name="Commercial Vendor Catalog Advisor",
            instructions=(
                "You help small commercial buyers compare vendor catalogs. "
                "For every product comparison, call compare_vendor_catalogs before answering. "
                "Use only the returned catalog data. Clearly separate lowest price from highest "
                "quality, mention material differences, and state when no catalog is available."
            ),
            mcp_servers=[server],
            model="gpt-oss",
        )
        result = await Runner.run(agent, question)
        return result.final_output


async def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the vendor catalog comparison agent a question.")
    parser.add_argument("question", nargs="?", default="Compare holiday string lights across the vendors.")
    args = parser.parse_args()
    print(await ask_agent(args.question))


if __name__ == "__main__":
    asyncio.run(main())
