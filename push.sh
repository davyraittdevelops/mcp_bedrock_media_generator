#!/bin/bash
set -e

# Configuration
DOCKER_USERNAME="davyraitt"
IMAGE_NAME="mcp_bedrock_media_generator"
TARGET_PLATFORM="linux/amd64"  # Force AMD64 for AWS/Linux servers

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🐳 Docker Multi-Platform Build Script${NC}"
echo "=================================="

# Check Docker buildx
if ! docker buildx version > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Setting up Docker buildx...${NC}"
    docker buildx create --name multiplatform --use
    docker buildx inspect --bootstrap
fi

# Get version
if git rev-parse --git-dir > /dev/null 2>&1; then
    GIT_HASH=$(git rev-parse --short HEAD)
    VERSION="v1.0.${GIT_HASH}"
else
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    VERSION="v1.0.${TIMESTAMP}"
fi

FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}"

echo -e "${BLUE}🔨 Building for platform: ${TARGET_PLATFORM}${NC}"

# Build and push for specific platform
docker buildx build \
    --platform ${TARGET_PLATFORM} \
    --tag "${FULL_IMAGE_NAME}:latest" \
    --tag "${FULL_IMAGE_NAME}:${VERSION}" \
    --push \
    .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Multi-platform build and push successful!${NC}"
    echo "📦 Image: ${FULL_IMAGE_NAME}:latest"
    echo "🏗️  Platform: ${TARGET_PLATFORM}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi