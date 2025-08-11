import os
import tempfile
import shutil
from typing import Dict, List, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from converter.registry import Registry

app = FastAPI(title="File Converter API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize registry
registry = Registry()

# MCP Protocol Models
class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Dict[str, Any] = {}
    error: Dict[str, Any] = None

# Validation endpoint for MCP
@app.post("/mcp/validate")
async def validate_token(bearer_token: str = Header(..., alias="authorization")):
    """Validate bearer token and return phone number for MCP authentication."""
    # Remove 'Bearer ' prefix if present
    token = bearer_token.replace("Bearer ", "") if bearer_token.startswith("Bearer ") else bearer_token
    
    # For demo purposes, returning a dummy phone number
    # In production, you would validate the token against your auth system
    if token:
        return {"phone": "919876543210"}  # Replace with actual phone validation
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

# MCP endpoint
@app.post("/mcp")
async def mcp_handler(request: MCPRequest):
    """Handle MCP protocol requests."""
    try:
        if request.method == "initialize":
            return MCPResponse(
                id=request.id,
                result={
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "file-converter",
                        "version": "1.0.0"
                    }
                }
            )
        
        elif request.method == "tools/list":
            tools = []
            
            # Get supported formats from all modules
            supported_conversions = []
            for module in registry.modules:
                formats = module.SUPPORTED_FORMATS
                for input_format in formats.get("input", []):
                    for output_format in formats.get("output", []):
                        if input_format != output_format:
                            supported_conversions.append(f"{input_format} to {output_format}")
            
            tools.append({
                "name": "convert_file",
                "description": f"Convert files between different formats. Supported conversions: {', '.join(supported_conversions)}",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "input_format": {
                            "type": "string",
                            "description": "Input file format (e.g., .pdf, .docx, .png)"
                        },
                        "output_format": {
                            "type": "string",
                            "description": "Output file format (e.g., .pdf, .docx, .png)"
                        },
                        "file_content": {
                            "type": "string",
                            "description": "Base64 encoded file content"
                        }
                    },
                    "required": ["input_format", "output_format", "file_content"]
                }
            })
            
            tools.append({
                "name": "list_supported_formats",
                "description": "List all supported input and output formats",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            })
            
            return MCPResponse(
                id=request.id,
                result={"tools": tools}
            )
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            arguments = request.params.get("arguments", {})
            
            if tool_name == "convert_file":
                return await handle_convert_file(request.id, arguments)
            elif tool_name == "list_supported_formats":
                return await handle_list_formats(request.id)
            else:
                return MCPResponse(
                    id=request.id,
                    error={"code": -32601, "message": f"Unknown tool: {tool_name}"}
                )
        
        else:
            return MCPResponse(
                id=request.id,
                error={"code": -32601, "message": f"Unknown method: {request.method}"}
            )
    
    except Exception as e:
        return MCPResponse(
            id=request.id,
            error={"code": -32603, "message": f"Internal error: {str(e)}"}
        )

async def handle_convert_file(request_id: str, arguments: Dict[str, Any]) -> MCPResponse:
    """Handle file conversion tool call."""
    try:
        import base64
        
        input_format = arguments.get("input_format")
        output_format = arguments.get("output_format")
        file_content = arguments.get("file_content")
        
        if not all([input_format, output_format, file_content]):
            return MCPResponse(
                id=request_id,
                error={"code": -32602, "message": "Missing required parameters"}
            )
        
        # Ensure formats start with dot
        if not input_format.startswith('.'):
            input_format = '.' + input_format
        if not output_format.startswith('.'):
            output_format = '.' + output_format
        
        # Find appropriate module
        module = None
        for mod in registry.modules:
            formats = mod.SUPPORTED_FORMATS
            if input_format in formats.get("input", []) and output_format in formats.get("output", []):
                module = mod
                break
        
        if not module:
            return MCPResponse(
                id=request_id,
                error={"code": -32602, "message": f"Conversion from {input_format} to {output_format} not supported"}
            )
        
        # Decode file content
        try:
            file_data = base64.b64decode(file_content)
        except Exception:
            return MCPResponse(
                id=request_id,
                error={"code": -32602, "message": "Invalid base64 file content"}
            )
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=input_format, delete=False) as input_temp:
            input_temp.write(file_data)
            input_path = input_temp.name
        
        with tempfile.NamedTemporaryFile(suffix=output_format, delete=False) as output_temp:
            output_path = output_temp.name
        
        try:
            # Perform conversion
            module.convert(input_path, output_path)
            
            # Read converted file
            with open(output_path, 'rb') as f:
                converted_data = f.read()
            
            # Encode to base64
            converted_base64 = base64.b64encode(converted_data).decode('utf-8')
            
            return MCPResponse(
                id=request_id,
                result={
                    "content": [{
                        "type": "text",
                        "text": f"File converted successfully from {input_format} to {output_format}. Converted file content (base64): {converted_base64}"
                    }]
                }
            )
        
        finally:
            # Cleanup temporary files
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    except Exception as e:
        return MCPResponse(
            id=request_id,
            error={"code": -32603, "message": f"Conversion failed: {str(e)}"}
        )

async def handle_list_formats(request_id: str) -> MCPResponse:
    """Handle list supported formats tool call."""
    try:
        formats_info = {}
        
        for module in registry.modules:
            module_name = module.__name__.split('.')[-1]
            formats_info[module_name] = module.SUPPORTED_FORMATS
        
        return MCPResponse(
            id=request_id,
            result={
                "content": [{
                    "type": "text",
                    "text": f"Supported formats by module:\n{formats_info}"
                }]
            }
        )
    
    except Exception as e:
        return MCPResponse(
            id=request_id,
            error={"code": -32603, "message": f"Failed to list formats: {str(e)}"}
        )

# Standard REST API endpoints
@app.get("/")
async def root():
    return {"message": "File Converter API", "version": "1.0.0"}

@app.get("/formats")
async def get_supported_formats():
    """Get all supported input and output formats."""
    formats = {}
    for module in registry.modules:
        module_name = module.__name__.split('.')[-1]
        formats[module_name] = module.SUPPORTED_FORMATS
    return formats

@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    output_format: str = Form(...)
):
    """Convert uploaded file to specified format."""
    if not output_format:
        raise HTTPException(status_code=400, detail="output_format is required")
    
    # Ensure output format starts with dot
    if not output_format.startswith('.'):
        output_format = '.' + output_format
    
    # Get input format from filename
    input_format = os.path.splitext(file.filename)[1].lower()
    
    # Find appropriate module
    module = None
    for mod in registry.modules:
        formats = mod.SUPPORTED_FORMATS
        if input_format in formats.get("input", []) and output_format in formats.get("output", []):
            module = mod
            break
    
    if not module:
        raise HTTPException(
            status_code=400, 
            detail=f"Conversion from {input_format} to {output_format} not supported"
        )
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(suffix=input_format, delete=False) as input_temp:
        content = await file.read()
        input_temp.write(content)
        input_path = input_temp.name
    
    output_filename = os.path.splitext(file.filename)[0] + output_format
    with tempfile.NamedTemporaryFile(suffix=output_format, delete=False) as output_temp:
        output_path = output_temp.name
    
    try:
        # Perform conversion
        module.convert(input_path, output_path)
        
        return FileResponse(
            output_path,
            filename=output_filename,
            media_type='application/octet-stream'
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    
    finally:
        # Cleanup input file
        if os.path.exists(input_path):
            os.unlink(input_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile=None, ssl_certfile=None)
