# Implementation scope: public repository vs. full product

Aqarmind is an AI-powered property advisory application. This repository is a **sanitized portfolio implementation**, **not** a dump of the full running production backend.

| Capability | In this public code | Notes |
| --- | --- | --- |
| FastAPI REST endpoints | **Yes** | `app/api/routes.py` |
| Azure OpenAI tool/function calling | **Yes** | Basic two-request tool execution pattern |
| Property search via Azure SQL | **Yes** | Parameterized queries; requires your database/schema |
| Mortgage calculations | **Yes** | Deterministic Python implementation |
| Azure AI Search keyword retrieval | **Yes** | Requires a pre-existing compatible index |
| Semantic Search | **Optional** | Requires `AZURE_SEARCH_SEMANTIC_CONFIG` and configured index |
| Azure AI Search vectors / hybrid retrieval | **No** | Not implemented in `app/services/search.py` |
| Tenant-aware RAG / document isolation | **No** | No tenant-scoped index query in this reference |
| Knowledge ingestion / embeddings pipeline | **No** | Not part of public code |
| Multi-turn memory / chat persistence | **No** | `session_id` is passed through, not persisted |
| Lead capture | **Yes** | SQL integration and consent check; not a complete abuse-prevention system |
| Docker packaging | **Included as reference** | Validate build and runtime locally |
| GitHub Actions unit/API test CI | **Yes** | Tests only; not automatic Azure deployment |
| Azure infrastructure provisioning / CI-CD | **No** | Not published here |
| OAuth, tenant authorization, rate limiting | **No** | Required before exposing this sample publicly |

## Context for technical reviewers

The full Aqarmind product has a broader architecture than this public reference, including tenant-aware knowledge retrieval and cloud application components. Specific production code, infrastructure configuration, internal prompts, datasets, and proprietary integrations are intentionally excluded. The features marked **No** above should not be inferred from this repository alone.

The aim of the public project is to show separation of concerns, functional tool dispatch, SQL-backed search, deterministic calculations, and responsible API design without publishing sensitive operational code.
