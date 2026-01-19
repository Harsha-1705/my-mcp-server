import os
import uvicorn
import requests
from io import BytesIO
from PIL import Image
from fastmcp import FastMCP
from playwright.async_api import async_playwright

# Initialize the Server
mcp = FastMCP("Web QA Agent")

# --- TOOL 1: THE SCOUT (Web Scraper) ---
@mcp.tool()
async def scrape_webpage(url: str) -> str:
    """
    Visits a URL, extracts text, and checks for basic errors (404/500).
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Web-QA-Agent/1.0")
        try:
            response = await page.goto(url, timeout=15000)
            status = response.status
            title = await page.title()
            content = await page.evaluate("document.body.innerText")
            return f"Status: {status}\nTitle: {title}\nContent Preview: {content[:800]}..."
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
        finally:
            await browser.close()

# --- TOOL 2: THE FIXER (Image Compressor) ---
@mcp.tool()
def compress_image(image_url: str, target_size_kb: int = 150) -> str:
    """
    Downloads an image from a URL, compresses it to the target size, and saves it.
    Returns the path to the optimized file.
    """
    try:
        # 1. Download the image
        response = requests.get(image_url)
        response.raise_for_status()
        
        # 2. Open and Compress
        img = Image.open(BytesIO(response.content))
        output_io = BytesIO()
        
        # Reduce quality until it fits (simple heuristic)
        quality = 85
        img.save(output_io, format='WEBP', quality=quality)
        while output_io.tell() > (target_size_kb * 1024) and quality > 10:
            output_io = BytesIO()
            quality -= 5
            img.save(output_io, format='WEBP', quality=quality)
            
        # 3. Save to disk (simulating a 'fixed' asset)
        filename = "optimized_image.webp"
        with open(filename, "wb") as f:
            f.write(output_io.getvalue())
            
        return f"SUCCESS. Image compressed from {len(response.content)/1024:.1f}KB to {output_io.tell()/1024:.1f}KB. Saved at: {os.path.abspath(filename)}"
    except Exception as e:
        return f"Error compressing image: {str(e)}"

# --- TOOL 3: THE SCRIBE (Jira Ticket Creator) ---
@mcp.tool()
def create_jira_ticket(summary: str, description: str, priority: str = "Medium") -> str:
    """
    Creates a Jira ticket. Requires JIRA_URL, JIRA_EMAIL, JIRA_TOKEN env vars.
    If env vars are missing, returns a simulated success message.
    """
    url = os.environ.get("JIRA_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_TOKEN")

    if not (url and email and token):
        return f"[SIMULATION] Ticket '{summary}' ({priority}) would be created. (Add JIRA_... env vars to Railway to make this real)."

    # Real API Call
    auth = (email, token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "fields": {
            "project": {"key": "WEB"}, # Change 'WEB' to your actual project Key
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"},
            "priority": {"name": priority}
        }
    }
    
    try:
        # Assuming standard Jira Cloud API structure
        api_endpoint = f"{url}/rest/api/3/issue"
        response = requests.post(api_endpoint, json=payload, auth=auth, headers=headers)
        if response.status_code == 201:
            key = response.json().get("key")
            return f"SUCCESS. Ticket created: {url}/browse/{key}"
        else:
            return f"FAILED to create ticket. Status: {response.status_code}. Response: {response.text}"
    except Exception as e:
        return f"Error connecting to Jira: {str(e)}"

# --- SERVER ENTRY POINT ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
