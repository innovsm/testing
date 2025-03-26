from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request, Response
import requests
import json
import os
mcp = FastMCP(
    "MyMCPDemo",
    description="A simple MCP server demo for Claude Desktop",
    version="1.0.0"
)

# Define a simple tool
@mcp.tool(name = "greet")
def greet(name: str = "anshu") -> str:  # Changed return type hint to dict
    """Greet a person by name"""
    return f"hello {name}"


# addinng github functions 
@mcp.tool(name="user_details", description="Provides user information")
def get_user_details(GITHUB_API_URL: str, username: str,HEADERS):
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return {"error": "Failed to fetch user details"}
    return response.json()
# Define a simple resource


# Create FastAPI app
app = FastAPI()

# HTTP endpoint to handle MCP messages
@app.post("/mcp/message")
async def mcp_endpoint(request: Request):
    try:
        # Read raw JSON request
        body = await request.json()
        tool_name = body.get("tool")
        tool_args = body.get("arguments", {})  # Default to empty dict if args missing
        
        response = await mcp.call_tool(name = tool_name,arguments= tool_args)
       
        
        # Convert TextContent to a serializable format
        return response
    except Exception as e:
        return e
# Health check endpoint for Render
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)