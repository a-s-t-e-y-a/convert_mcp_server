import os
import tempfile
import shutil
from typing import Dict, List, Any, Annotated
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import asyncio
from converter.registry import Registry
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent, INVALID_PARAMS, INTERNAL_ERROR
from mcp import ErrorData, McpError

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

# --- Auth Provider ---
class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="puch-client",
                scopes=["*"],
                expires_at=None,
            )
        return None

# --- MCP Server Setup ---
AUTH_TOKEN = "436eSs8id4Uj1D3CaQ6SVn4yDNxFX8tx3rezJXNw_BE"  # Your secure token
MY_NUMBER = "918840330283"  # Your phone number

mcp = FastMCP(
    "File Converter MCP Server",
    auth=SimpleBearerAuthProvider(AUTH_TOKEN),
)

# --- Tool: validate (required by Puch) ---
@mcp.tool
async def validate() -> str:
    return MY_NUMBER

# --- Tool: convert_file ---
@mcp.tool
async def convert_file(
    input_format: Annotated[str, Field(description="Input file format (e.g., pdf, docx, png)")],
    output_format: Annotated[str, Field(description="Output file format (e.g., pdf, docx, png)")],
    file_content: Annotated[str, Field(description="Base64 encoded file content")]
) -> str:
    """Convert files between different formats. Supports documents, images, videos, and audio."""
    try:
        import base64
        
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
            raise McpError(ErrorData(
                code=INVALID_PARAMS,
                message=f"Conversion from {input_format} to {output_format} not supported"
            ))
        
        # Decode file content
        try:
            file_data = base64.b64decode(file_content)
        except Exception:
            raise McpError(ErrorData(
                code=INVALID_PARAMS,
                message="Invalid base64 file content"
            ))
        
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
            
            return f"File converted successfully from {input_format} to {output_format}. Converted file content (base64): {converted_base64}"
        
        finally:
            # Cleanup temporary files
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    except McpError:
        raise
    except Exception as e:
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=f"Conversion failed: {str(e)}"
        ))

# --- Tool: list_supported_formats ---
@mcp.tool
async def list_supported_formats() -> str:
    """List all supported input and output formats for file conversion."""
    try:
        formats_info = {}
        
        for module in registry.modules:
            module_name = module.__name__.split('.')[-1]
            formats_info[module_name] = module.SUPPORTED_FORMATS
        
        # Format nicely for display
        result = "📋 **Supported File Conversion Formats:**\n\n"
        
        for module_name, formats in formats_info.items():
            result += f"**{module_name.replace('_', ' ').title()}:**\n"
            result += f"- Input: {', '.join(formats.get('input', []))}\n"
            result += f"- Output: {', '.join(formats.get('output', []))}\n\n"
        
        return result
    
    except Exception as e:
        raise McpError(ErrorData(
            code=INTERNAL_ERROR,
            message=f"Failed to list formats: {str(e)}"
        ))

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

# Standard REST API endpoints (legacy compatibility)
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
async def convert_file_legacy(
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

# --- Run MCP Server ---
async def main():
    print("🚀 Starting File Converter MCP server on http://0.0.0.0:8086")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)

if __name__ == "__main__":
    asyncio.run(main())
