# Security policy and disclosure

## Intended use

This is a **public portfolio reference**, not a hardened, deployable production API. Several endpoints are not authenticated, and the sample does not implement tenant authorization, rate limiting, or complete monitoring. Do not expose this version as a business service without the controls listed in [deployment notes](docs/deployment-notes.md).

## Repository hygiene

Do not commit real API keys, bearer tokens, SQL passwords, connection strings with credentials, private endpoints, certificates/private keys, customer/lead data, or private operational documents. Use `.env.example` for configuration names and place actual development secrets in a local ignored `.env` file. Never copy `.env` into a Docker image.

For Azure production workloads, prefer managed identity and a secure secret store where supported. Review logs to ensure lead data and tokens are not exposed. Treat frontend source as public and do not embed server secrets there.

**If a credential was committed**, assume it is compromised, revoke or rotate it, inspect access logs, and remove it from Git history. `.gitignore` does not remove previously committed values.

## Reporting

For a suspected vulnerability, contact the repository owner privately through the contact methods provided on their GitHub profile rather than publishing an exploit or credentials in an issue.
