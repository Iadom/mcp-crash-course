import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    logging.info(f"add({a}, {b})")
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio")