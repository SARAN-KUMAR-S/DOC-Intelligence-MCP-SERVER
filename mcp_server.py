# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastmcp>=3.4.2",
#     "groq>=1.4.0",
#     "httpx>=0.28.1",
#     "python-dotenv>=1.2.2",
#     "trafilatura>=2.1.0",
# ]
# ///

import json
import os
import httpx
import asyncio
import trafilatura
from dotenv import load_dotenv
from fastmcp import FastMCP
from groq import Groq

load_dotenv()

# Helper utilities (formerly in utils.py)
def clean_html_to_txt(html):
    try:  
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            favor_recall=False,
        )
        if extracted:
            return extracted
    except Exception as e:
        raise e

def get_response_from_llm(user_prompt, system_prompt, model):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment or .env file. Please define GROQ_API_KEY in your .env file.")

    # Map invalid/openai models to a valid Groq model (e.g., llama-3.1-8b-instant)
    if "openai" in model or "gpt-oss" in model:
        model = "llama-3.1-8b-instant"

    groq_client = Groq(api_key=api_key)
    chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model,
        )
    return chat_completion.choices[0].message.content


# MCP Server definition
mcp = FastMCP("docs")

SERPER_URL = "https://google.serper.dev/search"

async def search_web(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }  
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SERPER_URL, headers=headers, data=payload, timeout=30.0
        )
        response.raise_for_status()
        return response.json()


import sys

# Step2: Open official documentation
async def fetch_url(url: str):
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            # Strip HTML tags and extract readable text
            extracted_text = clean_html_to_txt(response.text)
            text_to_process = extracted_text if extracted_text else response.text
            return text_to_process
    except Exception as e:
        print(f"Error fetching URL {url}: {e}", file=sys.stderr)
        return None


from typing import Literal

# Step3: Read documentation and write code accordingly
docs_urls = {
    "langchain": "docs.langchain.com",
    "llama-index": "docs.llamaindex.ai",
    "openai": "platform.openai.com/docs",
    "uv": "docs.astral.sh/uv",
}

@mcp.tool()
async def get_docs(
    query: str, 
    library: Literal["uv", "openai", "langchain", "llama-index"]
):
    """
    Search the latest official documentation to answer developer queries.
    Use this tool whenever the user asks questions about uv, openai, langchain, or llama-index.

    Args:
        query: The search terms or query (e.g. "How to use publish a package with uv on gitlab")
        library: The specific library/technology to search for.
    """
    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported by this tool")
    
    query = f"site:{docs_urls[library]} {query}"

    results = await search_web(query)

    if not results or "organic" not in results or len(results["organic"]) == 0:
        return "No results found"
    
    text_parts = []
    for result in results["organic"]:
        link = result.get("link", "")
        raw = await fetch_url(link)
        if raw:
            labeled = f"SOURCE: {link}\n{raw}"
            text_parts.append(labeled)
    return "\n\n".join(text_parts)
        

def main():
    mcp.run(transport="stdio")
    

if __name__ == "__main__":
    main()