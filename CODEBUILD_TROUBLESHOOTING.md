# CodeBuild Troubleshooting Guide

## The Issue: Managed vs Custom Dockerfile

CodeBuild failed with:
```
error: No `pyproject.toml` found in current directory or any parent directory
```

### Root Cause

Your CodeBuild project is configured to use **AWS CodeBuild's managed image system** with special handlers/dockerfiles from S3. The error shows:

```
docker buildx build ... -f $CODEBUILD_SRC_DIR_DOCKERFILES/$RUNTIME
```

This uses CodeBuild's Lambda-style template (python3.13), NOT our custom `Dockerfile`.

## Two Solutions

### Solution 1: Use CodeBuild's Managed System (Current)

If you want to keep using CodeBuild's managed build system:

**What we did:**
- ✅ Added `pyproject.toml` (modern Python packaging)
- ✅ Updated `buildspec.yml` with proper build args

**What still needed:**
- Rebuild using this command (CodeBuild will now find pyproject.toml)
- Monitor logs for any remaining issues

### Solution 2: Use Our Custom Dockerfile (Recommended)

To skip CodeBuild's managed system and use our Dockerfile directly:

#### Step 1: Reconfigure CodeBuild Project

In AWS CodeBuild console:

1. Go to your project → Edit
2. **Environment section**:
   - Under "Additional configuration":
   - Find and **UNCHECK** any "Managed image" or "Environment image" option
   - Or change to use standard AWS image: `aws/codebuild/standard:7.0` (Ubuntu)

3. **Source section**:
   - Ensure "Buildspec" is set to: `buildspec.yml` (our file)
   - Not overridden by dropdown

4. **Click Update environment**

#### Step 2: Verify Settings

The buildspec.yml should have:
```yaml
phases:
  build:
    commands:
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG -f Dockerfile .
      - docker push $REPOSITORY_URI:$IMAGE_TAG
```

#### Step 3: Run Build Again

CodeBuild will now:
- ✅ Read OUR `buildspec.yml`
- ✅ Use OUR `Dockerfile` (not managed template)
- ✅ Build the BFI-MCP image
- ✅ Push to ECR

## What Changed in This Repo

### Added `pyproject.toml`
```toml
[project]
name = "bfi-mcp"
version = "0.1.0"
dependencies = ["mcp>=0.1.0"]
```

This satisfies CodeBuild's managed system requirements.

### Updated `buildspec.yml`
- Defines explicit build args for CodeBuild
- Uses our custom `Dockerfile` directly
- Handles ECR login and image tagging
- Generates `imagedefinitions.json` for deployment

## CodeBuild Project Configuration Checklist

When you configure (or reconfigure) your CodeBuild project:

### Source
- [ ] Repository: `github.com/OlivierAlter/BFI-MCP`
- [ ] Branch: `main`
- [ ] Buildspec name: `buildspec.yml`

### Environment
- [ ] Operating system: `Ubuntu`
- [ ] Runtime(s): `Standard`
- [ ] Image: `aws/codebuild/standard:7.0` (or latest)
- [ ] Image version: `Always use latest`
- [ ] Privileged: ✅ **ENABLED** (required for Docker)

### Service Role
- [ ] Has ECR push permissions
- [ ] Has ECR get-login-password permission

### Buildspec
- [ ] Using: `buildspec.yml`
- [ ] Not overridden in environment variables

## IAM Permissions Required

The CodeBuild service role needs these ECR permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRAuth",
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    },
    {
      "Sid": "ECRPush",
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:BatchCheckLayerAvailability"
      ],
      "Resource": "arn:aws:ecr:*:YOUR_ACCOUNT_ID:repository/bfi-mcp"
    }
  ]
}
```

## Debugging CodeBuild Failures

1. **Check CodeBuild logs**: AWS console → CodeBuild → Your project → Build history
2. **View CloudWatch logs**: CodeBuild provides detailed logs in CloudWatch
3. **Test locally first**: `docker build -t bfi-mcp:latest .`
4. **Verify Dockerfile**: Our Dockerfile is in repo root, simple multi-stage build
5. **Check buildspec.yml syntax**: `yamllint buildspec.yml` or validate in console

## Next Steps

1. **Update CodeBuild project** (if using managed images):
   - Remove managed image constraints
   - Point to standard environment
   - Enable privileged mode

2. **Run build again**:
   - CodeBuild will use our `buildspec.yml`
   - Build image from our `Dockerfile`
   - Push to ECR with proper tags

3. **Monitor logs**:
   - Watch for "Building Docker image..."
   - Should complete in ~1-2 minutes
   - Image will be tagged with commit hash + "latest"

## Questions?

The structure is now:
- `Dockerfile` - Production container definition
- `buildspec.yml` - CodeBuild instructions
- `pyproject.toml` - Python package metadata
- `requirements.txt` - Pip dependencies (fallback)

All three work together to provide flexibility in how the build is triggered and executed.

---

**Status**: Ready for CodeBuild deployment
**Last Updated**: November 8, 2025
