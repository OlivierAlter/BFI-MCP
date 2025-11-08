# CodeBuild Troubleshooting Guide

## The Issue: CodeBuild Managed System Overrides buildspec.yml

CodeBuild is failing because it's using **AWS CodeBuild's managed build system** which completely ignores our custom `buildspec.yml` and uses its own handlers from S3.

The error sequence:
```
YAML location is /codebuild/readonly/buildspec.yml  ← CodeBuild's managed spec
-f $CODEBUILD_SRC_DIR_DOCKERFILES/$RUNTIME          ← CodeBuild's managed Dockerfile
error: Unable to find lockfile at `uv.lock`          ← Expecting uv package manager
```

### Root Cause

Your CodeBuild project is configured with **CodeBuild's managed handlers system** which:
1. Ignores your repository's buildspec.yml
2. Uses pre-made Dockerfiles from S3 (`$CODEBUILD_SRC_DIR_DOCKERFILES`)
3. Expects specific file formats (uv.lock for Python)
4. Runs its own pre-build/build/post-build commands

This is a special CodeBuild feature for "managed builds" - it must be disabled for custom projects.

## THE FIX: Disable CodeBuild's Managed System

### Step-by-Step Instructions

#### Step 1: Go to CodeBuild Project Settings

1. Open AWS CodeBuild console
2. Find your project for BFI-MCP
3. Click **Edit** button
4. Select **Edit source**

#### Step 2: Configure Source Settings

In the **Source** section:

- **Repository**: `github.com/OlivierAlter/BFI-MCP` ✓
- **Branch**: `main` ✓
- **Buildspec name**: `buildspec.yml` ← **IMPORTANT: Type this explicitly**
  - Don't leave it blank
  - Don't use "Insert build commands"
  - Type: `buildspec.yml`

**Click "Update source"**

#### Step 3: Configure Environment

Click **Edit** → **Edit environment**

In the **Environment** section:

1. **Operating system**: Ubuntu
2. **Runtime(s)**: Standard
3. **Image**: `aws/codebuild/standard:7.0` (Ubuntu standard image)
4. **Image version**: Always use latest
5. **Privileged**: ✅ **ENABLED** (required for Docker)

**Do NOT select**:
- ❌ Any "managed" handlers
- ❌ "Managed image" options
- ❌ CodeBuild's Lambda build images

#### Step 4: Save & Run Build

Click **Update environment** to save

Then trigger a new build - CodeBuild will now:
- ✅ Read our `buildspec.yml` from the repo
- ✅ Use our custom `Dockerfile`
- ✅ Build and push the image
- ✅ Run tests inside the container

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

## Quick Checklist

After following the steps above, verify:

- [ ] **Source Buildspec**: Set to `buildspec.yml` (typed explicitly)
- [ ] **Environment Image**: Ubuntu `aws/codebuild/standard:7.0`
- [ ] **Privileged Mode**: ✅ Enabled
- [ ] **No managed handlers**: Disabled
- [ ] **ECR Repository**: Created with name `bfi-mcp`
- [ ] **IAM Role**: Has ECR push permissions (see below)

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
