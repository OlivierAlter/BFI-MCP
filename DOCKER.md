# BFI-MCP Docker Deployment

This guide covers building, running, and deploying the BFI-MCP as a Docker container.

## Quick Start

### Build the Image Locally

```bash
docker build -t bfi-mcp:latest .
```

### Run the Container

```bash
docker run -it bfi-mcp:latest
```

Or using Docker Compose:

```bash
docker-compose up --build
```

## Image Details

- **Base Image**: `python:3.11-slim`
- **Size**: ~180-200 MB (optimized multi-stage build)
- **Entrypoint**: `python mcp_server.py`
- **Health Check**: Enabled with 30s intervals

## AWS CodeBuild Deployment

The `buildspec.yml` is configured for AWS CodeBuild with ECR (Elastic Container Registry).

### Prerequisites

1. **AWS Account** with ECR repository
2. **CodeBuild Project** configured with:
   - Source: GitHub (this repository)
   - Environment: Managed image (aws/codebuild/standard:7.0)
   - Service role with ECR permissions

### Setup Steps

#### 1. Create ECR Repository

```bash
aws ecr create-repository --repository-name bfi-mcp --region us-east-1
```

#### 2. Update buildspec.yml

Replace `REPLACE_WITH_YOUR_ACCOUNT_ID` with your AWS account ID:

```bash
sed -i 's/REPLACE_WITH_YOUR_ACCOUNT_ID/123456789012/' buildspec.yml
```

Or manually edit the `AWS_ACCOUNT_ID` variable.

#### 3. Configure CodeBuild

Create a CodeBuild project with:
- **Source**: GitHub repository (OlivierAlter/BFI-MCP)
- **Environment**:
  - Managed image: `aws/codebuild/standard:7.0`
  - Privileged: ✅ (required for Docker)
- **Source version**: `main`
- **Buildspec**: `buildspec.yml`

#### 4. Add IAM Permissions

The CodeBuild service role needs ECR permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:*:ACCOUNT_ID:repository/bfi-mcp"
    },
    {
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    }
  ]
}
```

### Build with CodeBuild

Once configured, CodeBuild will:
1. Pull the latest code from GitHub
2. Build the Docker image
3. Run tests inside the container
4. Push to ECR with commit hash and `latest` tags
5. Generate `imagedefinitions.json` for deployment

### Monitor Build

```bash
aws codebuild batch-get-builds --ids <build-id> --region us-east-1
```

## Running in Production

### Using Docker

```bash
docker run -d \
  --name bfi-mcp \
  --restart unless-stopped \
  bfi-mcp:latest
```

### Using ECR Image

```bash
docker run -d \
  --name bfi-mcp \
  --restart unless-stopped \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/bfi-mcp:latest
```

### Using Docker Compose

```bash
docker-compose up -d
```

## Updating Data

When new BFI guides are released:

1. **Locally**: Copy new JSON files to `data/`
2. **Rebuild**: `docker build -t bfi-mcp:latest .`
3. **Test**: `docker run -it bfi-mcp:latest python test.py`
4. **Push**: `docker push <image-uri>`

## Advanced Configuration

### Environment Variables

Add to `docker-compose.yml` or `docker run`:

```bash
docker run \
  -e PYTHONUNBUFFERED=1 \
  -e PYTHONDONTWRITEBYTECODE=1 \
  bfi-mcp:latest
```

### Volume Mounts

Mount data from host:

```bash
docker run -v /path/to/data:/app/data:ro bfi-mcp:latest
```

### Network Configuration

For MCP communication over network (not typical for stdio):

```bash
docker run \
  --network host \
  bfi-mcp:latest
```

## Troubleshooting

### Build Fails

Check CodeBuild logs:
```bash
aws codebuild batch-get-builds \
  --ids <build-id> \
  --region us-east-1 \
  --query 'builds[0].logs.cloudWatchLogs.groupName'
```

### Container Won't Start

Check logs:
```bash
docker logs bfi-mcp
```

### Tests Fail

Run locally:
```bash
docker run --rm bfi-mcp:latest python test.py
```

### ECR Push Fails

Verify credentials:
```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

## File Structure

```
bfi-mcp/
├── Dockerfile              # Multi-stage build configuration
├── .dockerignore          # Files to exclude from build
├── docker-compose.yml     # Docker Compose configuration
├── buildspec.yml          # AWS CodeBuild specification
├── DOCKER.md              # This file
├── mcp_server.py          # MCP server
├── data_loader.py         # Data loading logic
├── filters.py             # Filtering logic
├── data/                  # Film data
└── requirements.txt       # Python dependencies
```

## Performance Notes

- **Image Size**: ~180-200 MB (slim Python base)
- **Build Time**: ~2-3 minutes
- **Startup Time**: <2 seconds
- **Memory Usage**: ~50-100 MB at runtime

## Security Considerations

- Uses slim Python base image (smaller attack surface)
- Data mounted as read-only in compose
- No exposed ports (stdio-based MCP)
- No secrets in image (configure separately if needed)

---

**Status**: ✅ Ready for Docker deployment
**Last Updated**: November 8, 2025
