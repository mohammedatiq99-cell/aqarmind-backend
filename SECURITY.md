# Security Policy

## Public repository rules

Do not commit:

- API keys or access tokens
- Azure SQL credentials
- connection strings containing credentials
- private endpoints intended to remain confidential
- certificates or private keys
- production customer / lead data
- private prompt or business-policy content that should remain internal

Use `.env.example` for variable names only and store real values in a local `.env` file or a secure secret store.

For Azure production workloads, prefer managed identity and Azure Key Vault where supported.

If a credential is accidentally committed, treat it as compromised: revoke or rotate it immediately, remove it from Git history, and review relevant audit logs.
