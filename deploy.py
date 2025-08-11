#!/usr/bin/env python3
"""
Production deployment script for the File Converter MCP Server
Supports HTTPS with SSL certificates
"""
import uvicorn
import os
import sys
from main import app

def main():
    # Configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    
    # SSL Configuration
    ssl_keyfile = os.getenv('SSL_KEYFILE')
    ssl_certfile = os.getenv('SSL_CERTFILE')
    
    # Check if SSL files exist if specified
    if ssl_keyfile and ssl_certfile:
        if not os.path.exists(ssl_keyfile):
            print(f"Error: SSL key file not found: {ssl_keyfile}")
            sys.exit(1)
        if not os.path.exists(ssl_certfile):
            print(f"Error: SSL certificate file not found: {ssl_certfile}")
            sys.exit(1)
        
        print(f"Starting HTTPS server on {host}:{port}")
        uvicorn.run(
            app, 
            host=host, 
            port=port, 
            ssl_keyfile=ssl_keyfile, 
            ssl_certfile=ssl_certfile,
            reload=False
        )
    else:
        print(f"Starting HTTP server on {host}:{port}")
        print("Warning: Running without HTTPS. For production, set SSL_KEYFILE and SSL_CERTFILE environment variables.")
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            reload=False
        )

if __name__ == "__main__":
    main()
