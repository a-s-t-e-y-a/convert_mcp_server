#!/usr/bin/env python3
"""
MCP Server Verification Script
Tests all MCP endpoints and validates compatibility with Puch AI requirements
"""
import requests
import json
import base64
import sys

def test_mcp_server(base_url="http://localhost:8000"):
    """Test all MCP endpoints"""
    
    print(f"Testing MCP Server at: {base_url}")
    print("=" * 50)
    
    # Test 1: Basic server health
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Server Health: {response.json()}")
    except Exception as e:
        print(f"✗ Server Health Failed: {e}")
        return False
    
    # Test 2: Token validation (required by Puch AI)
    try:
        response = requests.post(
            f"{base_url}/mcp/validate",
            headers={"Authorization": "Bearer test_token_123"}
        )
        if response.status_code == 200:
            data = response.json()
            if "phone" in data:
                print(f"✓ Token Validation: {data['phone']}")
            else:
                print("✗ Token Validation: Missing phone number")
                return False
        else:
            print(f"✗ Token Validation Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Token Validation Error: {e}")
        return False
    
    # Test 3: MCP Initialize
    try:
        response = requests.post(
            f"{base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "1",
                "method": "initialize",
                "params": {}
            }
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("result", {}).get("serverInfo", {}).get("name") == "file-converter":
                print("✓ MCP Initialize: Success")
            else:
                print("✗ MCP Initialize: Invalid response")
                return False
        else:
            print(f"✗ MCP Initialize Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ MCP Initialize Error: {e}")
        return False
    
    # Test 4: Tools List
    try:
        response = requests.post(
            f"{base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "2",
                "method": "tools/list",
                "params": {}
            }
        )
        if response.status_code == 200:
            data = response.json()
            tools = data.get("result", {}).get("tools", [])
            if len(tools) >= 2:  # Should have convert_file and list_supported_formats
                print(f"✓ Tools List: {len(tools)} tools available")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description'][:80]}...")
            else:
                print("✗ Tools List: Insufficient tools")
                return False
        else:
            print(f"✗ Tools List Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Tools List Error: {e}")
        return False
    
    # Test 5: List Formats Tool
    try:
        response = requests.post(
            f"{base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "3",
                "method": "tools/call",
                "params": {
                    "name": "list_supported_formats",
                    "arguments": {}
                }
            }
        )
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                print("✓ List Formats Tool: Success")
            else:
                print("✗ List Formats Tool: No result")
                return False
        else:
            print(f"✗ List Formats Tool Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ List Formats Tool Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All MCP tests passed!")
    print("\nYour server is ready for Puch AI integration!")
    print("\nNext steps:")
    print("1. Deploy to a public HTTPS endpoint")
    print("2. Use this command in Puch AI:")
    print("   /mcp connect https://your-server.com/mcp your_bearer_token")
    
    return True

def test_file_conversion(base_url="http://localhost:8000"):
    """Test file conversion capability"""
    print("\nTesting File Conversion...")
    
    # Create a simple test image (1x1 PNG)
    test_png = base64.b64encode(
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x007n\xf9$\x00\x00\x00\nIDAT\x08\x1dc\xf8\x00\x00\x00\x01\x00\x01u\xcc\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    ).decode('utf-8')
    
    try:
        response = requests.post(
            f"{base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": "4",
                "method": "tools/call",
                "params": {
                    "name": "convert_file",
                    "arguments": {
                        "input_format": ".png",
                        "output_format": ".jpg",
                        "file_content": test_png
                    }
                }
            }
        )
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                print("✓ File Conversion Test: Success")
                return True
            else:
                print("✗ File Conversion Test: No result")
                return False
        else:
            print(f"✗ File Conversion Test Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ File Conversion Test Error: {e}")
        return False

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    success = test_mcp_server(base_url)
    if success:
        test_file_conversion(base_url)
    else:
        print("\n✗ MCP server tests failed!")
        sys.exit(1)
