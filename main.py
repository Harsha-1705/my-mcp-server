{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import uvicorn\
from fastmcp import FastMCP\
\
# Initialize the Server\
# "dependencies" auto-installs if missing, but requirements.txt handles that on Railway.\
mcp = FastMCP("Web QA Agent")\
\
# --- TOOL DEFINITIONS (Placeholders for now) ---\
@mcp.tool()\
def compress_image(image_url: str, target_size_kb: int = 150) -> str:\
    """Compresses an image to a target size."""\
    return f"Simulated compression of \{image_url\} to \{target_size_kb\}KB"\
\
@mcp.tool()\
def scrape_url_visual(url: str) -> str:\
    """Scouts a URL for visual defects."""\
    return f"Simulated scraping of \{url\}. Found 3 defects."\
\
@mcp.tool()\
def create_jira_ticket(summary: str, priority: str) -> str:\
    """Creates a Jira ticket."""\
    return f"Ticket created: \{summary\} (\{priority\})"\
\
# --- SERVER ENTRY POINT ---\
if __name__ == "__main__":\
    # Railway provides the PORT variable. Default to 8000 if local.\
    port = int(os.environ.get("PORT", 8000))\
    \
    # We use mcp.run(transport="sse") to make it a web server\
    mcp.run(transport="sse", host="0.0.0.0", port=port)}