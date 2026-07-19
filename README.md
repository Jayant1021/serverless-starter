# Serverless Starter

A minimal AWS SAM starter for a Python Lambda behind API Gateway with a push-to-deploy pipeline.

## Files

- `src/app.py` - Lambda handler
- `template.yaml` - AWS infrastructure
- `samconfig.toml` - SAM deploy defaults
- `buildspec.yml` - CodeBuild commands for the pipeline
- `.gitignore` - Local build and cache files

## Deploy

```bash
sam build
sam deploy --guided
```

## Endpoints

- `GET /` - sample response
- `GET /health` - health check
