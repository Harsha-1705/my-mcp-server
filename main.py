import os
import uvicorn
from fastmcp import FastMCP
from playwright.async_api import async_playwright

# Initialize the Server
mcp = FastMCP("Web QA Agent")

# --- TOOL 1: THE SCOUT (Real Browser) ---
@mcp.tool()
async def scrape_webpage(url: str) -> str:
    """
    Visits a URL using a headless browser and extracts its content for inspection.
    Returns the page title, HTTP status, and visible text.
    """
    async with async_playwright() as p:
        # Launch browser (headless means no visible UI, faster for servers)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Web-QA-Agent/1.0")
        page = await context.new_page()
        
        try:
            # Go to the URL (wait up to 10 seconds)
            response = await page.goto(url, timeout=10000)
            status = response.status
            title = await page.title()
            
            # Get the text content (what the user sees)
            content = await page.evaluate("document.body.innerText")
            
            # Get all links (for the crawler to find next steps)
            links = await page.evaluate("""
                Array.from(document.querySelectorAll('a')).map(a => a.href)
            """)
            
            # Clean up the output for the LLM
            report = f"--- REPORT FOR: {url} ---\n"
            report += f"Status Code: {status}\n"
            report += f"Page Title: {title}\n"
            report += f"Visible Text Preview: {content[:500]}...\n" # First 500 chars
            report += f"Found {len(links)} Links.\n"
            
            return report

        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
            
        finally:
            await browser.close()

# --- TOOL 2: THE FIXER (Image Compressor - Placeholder) ---
@mcp.tool()
def compress_image(image_url: str, target_size_kb: int = 150) -> str:
    """Compresses an image to a target size."""
    return f"Simulated compression of {image_url} to {target_size_kb}KB"

# --- TOOL 3: THE SCRIBE (Jira - Placeholder) ---
@mcp.tool()
def create_jira_ticket(summary: str, priority: str) -> str:
    """Creates a Jira ticket."""
    return f"Ticket created: {summary} ({priority})"

# --- SERVER ENTRY POINT ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Railway internal port is often 8080, but let's stick to the env var
    mcp.run(transport="sse", host="0.0.0.0", port=port)
