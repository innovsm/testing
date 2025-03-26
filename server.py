from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request, Response
import json
import asyncio
import os

# Create MCP server instance
mcp = FastMCP(
    "MyMCPDemo",
    description="A simple MCP server demo for Claude Desktop",
    version="1.0.0"
)

# Define a simple tool
@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name"""
    return f"Hello, {name}! Welcome to my MCP server on Render."

# Define a simple resource
@mcp.resource("info://welcome")
def get_welcome() -> str:
    """Get welcome message"""
    return "Welcome to the MCP server hosted on Render!"

# Create FastAPI app
app = FastAPI()

# HTTP endpoint to handle MCP messages
@app.post("/mcp/message")
async def mcp_endpoint(request: Request):
    # Read raw JSON request
    body = await request.json()
    
    # Process the request through FastMCP
    response = await mcp.handle_message(body)
    
    # Return JSON response
    return Response(
        content=json.dumps(response),
        media_type="application/json"
    )

# Health check endpoint for Render
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Start the MCP server event loop
async def start_mcp():
    await mcp.start()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_mcp())

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)