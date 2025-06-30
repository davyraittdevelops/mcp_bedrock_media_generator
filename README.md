# mcp_bedrock_media_generator

Fixed version of an MCP server for generating images with MCP / Bedrock

# AWS Bedrock Media Generator MCP Server

A Model Context Protocol (MCP) server for generating images and videos using Amazon Bedrock's Nova Canvas and Nova Reel models. Designed specifically for LibreChat's MCP image generation feature.

## Features

- **Image Generation**: High-quality images using Amazon Nova Canvas
- **Video Generation**: Video creation using Amazon Nova Reel
- **LibreChat Compatible**: Returns images in proper MCP format for inline display
- **SSE Transport**: Server-Sent Events for real-time communication
- **Docker Ready**: Easy deployment with Docker/Docker Compose
- **AWS Integration**: Direct integration with AWS Bedrock services

## Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the container
docker run -d -p 8961:8961 \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_REGION=us-east-1 \
  --name mcp-media-generator \
  davyraitt/mcp_bedrock_media_generator:latest
```

### Using Docker Compose

```yaml
version: "3.8"
services:
  mcp-media-generator:
    image: davyraitt/mcp_bedrock_media_generator:latest
    container_name: mcp-media-generator
    restart: unless-stopped
    ports:
      - "8961:8961"
    environment:
      - AWS_ACCESS_KEY_ID=your_access_key
      - AWS_SECRET_ACCESS_KEY=your_secret_key
      - AWS_REGION=us-east-1
```

## LibreChat Integration

Add to your LibreChat `librechat.yaml`:

```yaml
mcpServers:
  media-creator:
    type: sse
    url: http://localhost:8961/sse
    timeout: 120000
    initTimeout: 30000
    serverInstructions: |
      Use these tools for AI media generation with Amazon Nova models:
      - Generate high-quality images using Amazon Nova Canvas
      - Create videos using Amazon Nova Reel
      - Customize dimensions, quality, and creative parameters
      - Images are displayed directly in the chat interface
      - Support for various aspect ratios and creative styles
```

## Environment Variables

| Variable              | Description           | Required | Default   |
| --------------------- | --------------------- | -------- | --------- |
| AWS_ACCESS_KEY_ID     | AWS Access Key ID     | Yes      | -         |
| AWS_SECRET_ACCESS_KEY | AWS Secret Access Key | Yes      | -         |
| AWS_REGION            | AWS Region            | No       | us-east-1 |

## Available Tools

### create-image

Generate images using Amazon Nova Canvas

**Parameters:**

- `prompt` (required): Text description of the image
- `negative_prompt` (optional): What to avoid in the image
- `quality` (optional): "standard" or "premium"
- `width` (optional): Image width (320-4096)
- `height` (optional): Image height (320-4096)
- `seed_value` (optional): Seed for reproducible results

### create-video

Generate videos using Amazon Nova Reel

**Parameters:**

- `prompt` (required): Text description of the video

## Prerequisites

- AWS Account with Bedrock access
- Nova Canvas and Nova Reel models enabled in your AWS region
- Appropriate IAM permissions for Bedrock access

## Development

### Building from Source

```bash
# Clone the repository
git clone <your-repo-url>
cd mcp_bedrock_media_generator

# Build Docker image
docker build -t davyraitt/mcp_bedrock_media_generator:latest .

# Run locally
docker run -p 8961:8961 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  davyraitt/mcp_bedrock_media_generator:latest
```

### Auto-Deploy Script

Use the included `deploy.sh` script to automatically build and push updates:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Troubleshooting

### Common Issues

- **"Model not found" errors**: Ensure Nova Canvas/Reel models are enabled in your AWS region
- **Permission denied**: Check IAM permissions for Bedrock access
- **Connection timeout**: Increase timeout values in LibreChat configuration
- **Images not displaying**: Verify you're using the latest version with MCP image format support

### Health Check

The server provides a health check endpoint:

```bash
GET http://localhost:8961/sse
```

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Support

For issues and support:

- **GitHub Issues**: Create an issue
- **Docker Hub**: davyraitt/mcp_bedrock_media_generator
