from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request, Response
import json
import os

# Create MCP server instance
mcp = FastMCP(
    "MyMCPDemo",
    description="A simple MCP server demo for Claude Desktop",
    version="1.0.0"
)

# Define a simple tool
@mcp.tool(name = "greet")
def greet(name: str = "anshu") -> dict:  # Changed return type hint to dict
    """Greet a person by name"""

    return {"result": f"Hello, {name}! Welcome to my MCP server on Render."}

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
    try:
        # Read raw JSON request
        body = await request.json()

        
        # Process the request through FastMCP
        response = await mcp.call_tool(name = "greet" , arguments = "")
       
        
        # Convert TextContent to a serializable format
        if hasattr(response, 'text'):  # Check if it has a 'text' attribute
            serializable_response = response.text
        elif isinstance(response, dict):  # Already a dict
            serializable_response = response
        else:  # Fallback: convert to string
            serializable_response = str(response)
        
       
        
        # Return JSON response
        return Response(
            content=json.dumps(serializable_response),
            media_type="application/json"
        )
    except Exception as e:
       
        return Response(
            content=json.dumps({"error": str(e)}),
            media_type="application/json",
            status_code=500
        )
# Health check endpoint for Render
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)