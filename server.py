
from mcp.server.fastmcp import FastMCP
import requests
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
mcp = FastMCP(
    "MyMCPDemo",
    description="A simple MCP server demo for Claude Desktop",
    version="1.0.0"
)

# Define a simple tool
@mcp.tool(name="greet")
def greet(name: str = "anshu") -> str:
    """Greet a person by name"""
    logger.info(f"Calling greet with name: {name}")
    return f"hello {name}"

# Adding GitHub functions
@mcp.tool(name="user_details", description="Provides user information")
def get_user_details(GITHUB_API_URL: str, username: str, HEADERS: dict) -> dict:
    """Fetch GitHub user details"""
    url = f"{GITHUB_API_URL}/users/{username}"
    logger.info(f"Fetching GitHub user details from {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        logger.error(f"Failed to fetch user details: {response.status_code}")
        return {"error": "Failed to fetch user details"}
    return response.json()

# Run the MCP server
if __name__ == "__main__":

    # Assuming FastMCP has a run method to start its own serve  
    mcp.run(transport="sse")