#!/usr/bin/env python3
"""
Start the File Converter MCP Server
"""
import uvicorn
from main import app

if __name__ == "__main__":
    # For HTTPS in production, you would add ssl_keyfile and ssl_certfile
    # uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")
    uvicorn.run(app, host="0.0.0.0", port=8000)
