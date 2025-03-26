
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.tool(name ="bmi")
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


# Run the MCP server

if __name__ == "__main__":
    mcp.run(transport="stdio")


# The server will be running on http://localhost:8080/