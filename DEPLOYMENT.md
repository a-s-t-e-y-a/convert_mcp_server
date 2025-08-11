# File Converter MCP Server

A FastAPI-based file converter that serves as an MCP (Model Context Protocol) server compatible with Puch AI.

## Supported Conversions

### Images
- PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP ↔ PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

### Documents  
- PDF → DOCX
- DOCX → PDF
- PDF, DOCX → TXT

### Audio
- MP3, WAV, OGG, FLAC, AAC, M4A ↔ MP3, WAV, OGG, FLAC, AAC, M4A

### Video
- MP4, AVI, MOV, MKV, WMV, FLV, WEBM, GIF ↔ MP4, AVI, MOV, MKV, WMV, FLV, WEBM, GIF

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Run the server:
```bash
uv run python main.py
```

3. For production with HTTPS:
```bash
# Set SSL environment variables
export SSL_KEYFILE=/path/to/your/private.key
export SSL_CERTFILE=/path/to/your/certificate.crt
export HOST=0.0.0.0
export PORT=443

uv run python deploy.py
```

## Connecting to Puch AI

1. Deploy your server on a platform like Vercel, Railway, or any cloud provider that supports HTTPS
2. Get your server's HTTPS URL (e.g., https://your-converter.vercel.app)
3. In Puch AI chat, use the command:

```
/mcp connect https://your-converter.vercel.app/mcp your_bearer_token
```

Replace `your_bearer_token` with any token. The server will validate it and return phone number `919876543210` for demo purposes.

## Available MCP Tools

1. **convert_file** - Convert files between different formats
   - Parameters: input_format, output_format, file_content (base64)

2. **list_supported_formats** - List all supported conversion formats

## API Endpoints

- `GET /` - Server info
- `GET /formats` - List supported formats
- `POST /convert` - Convert file (multipart upload)
- `POST /mcp/validate` - MCP token validation
- `POST /mcp` - MCP protocol endpoint

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `SSL_KEYFILE` - Path to SSL private key
- `SSL_CERTFILE` - Path to SSL certificate

## Production Deployment

For Puch AI compatibility, your server MUST:
1. Serve over HTTPS
2. Be publicly accessible
3. Have a `validate` tool that returns a phone number when given a bearer token

The server includes all required MCP protocol implementation and is ready for production deployment.
