import os
import uvicorn
from fastmcp import FastMCP

# Initialize the Server
mcp = FastMCP("Web QA Agent")

# --- TOOL DEFINITIONS ---
@mcp.tool()
def compress_image(image_url: str, target_size_kb: int = 150) -> str:
    """Compresses an image to a target size."""
    return f"Simulated compression of {image_url} to {target_size_kb}KB"

@mcp.tool()
def scrape_url_visual(url: str) -> str:
    """Scouts a URL for visual defects."""
    return f"Simulated scraping of {url}. Found 3 defects."

@mcp.tool()
def create_jira_ticket(summary: str, priority: str) -> str:
    """Creates a Jira ticket."""
    return f"Ticket created: {summary} ({priority})"

# --- SERVER ENTRY POINT ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
