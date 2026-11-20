# Packaging and deployment notes

## Local development

Install Python dependencies with `pip install -r requirements.txt`, copy `.env.example` to `.env`, and start `uvicorn app.main:app --reload`.

Azure OpenAI, Azure AI Search, and Azure SQL calls require **your own** resources. You can still exercise `/health`, `/config-check`, and `/mortgage` without credentials.

For SQL endpoints, the database requires tables/columns matching `app/services/database.py` and the Microsoft ODBC Driver 18 installed on the host.

## Docker reference

```bash
docker build -t aqarmind-backend:portfolio .
docker run --rm -p 8000:8000 aqarmind-backend:portfolio
```

When ready to connect dev resources:

```bash
docker run --rm -p 8000:8000 --env-file .env aqarmind-backend:portfolio
```

The multi-stage Dockerfile uses Python 3.11 on Debian 12, installs dependencies in a builder stage, and installs Microsoft ODBC Driver 18 in the runtime image. It runs the application as a non-root user and supplies an HTTP health check. Installation is based on [Microsoft's Linux ODBC instructions](https://learn.microsoft.com/en-us/sql/connect/odbc/linux/installing-the-microsoft-odbc-driver-for-sql-server-on-linux). **The Docker build was not executed in the environment where this portfolio package was prepared; verify it locally before deploying.**

## GitHub Actions

`.github/workflows/ci.yml` compiles Python and runs the test suite on `main` changes and pull requests. It does **not** push images, provision Azure resources, or deploy to production.

## Before any actual public deployment

- Implement real authentication and authorization (including tenant-level checks).
- Protect `/config-check`, `/leads`, and other endpoints as appropriate for the threat model.
- Add rate limiting, quotas, logging/redaction, request tracing, and abuse protection.
- Use managed identity and/or a secret manager when supported; never place keys in images or git.
- Validate database permissions and schema migrations.
- Evaluate prompt injection, tool schema validation, retries/timeouts, and tool output limits.
- Validate Docker images and dependencies with vulnerability scans and regression tests.
- Configure CORS for the intended frontend only; don't treat CORS as authentication.
