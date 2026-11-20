# Architecture and design decisions

This document describes the **code in this public repository**. Production-only features are noted separately in [implementation scope](implementation-scope.md).

## Public reference implementation

```mermaid
sequenceDiagram
    participant Client as Web client
    participant API as FastAPI (/chat)
    participant Azure as Azure OpenAI
    participant Tools as Tool dispatcher
    participant SQL as Azure SQL
    participant Search as Azure AI Search

    Client->>API: POST /chat {session_id, message}
    API->>API: Validate message length
    API->>Azure: System prompt + user question + tool definitions
    Azure-->>API: Text response or tool calls
    opt Tool calls requested
        loop Each approved tool call
            API->>Tools: Parse name and arguments
            alt Structured property query
                Tools->>SQL: Parameterized SELECT
                SQL-->>Tools: Property records
            else Knowledge question
                Tools->>Search: Text query (optional semantic)
                Search-->>Tools: Search snippets
            else Mortgage estimate
                Tools->>Tools: Deterministic calculation
            end
            Tools-->>API: Tool result
        end
        API->>Azure: User request + tool results
        Azure-->>API: Final answer
    end
    API-->>Client: {answer, session_id}
```

The chat workflow is implemented in `app/services/ai.py`. Tools are defined and dispatched in `app/tools/property_tools.py`.

## Why the boundaries matter

| Component | Role | Rationale |
| --- | --- | --- |
| Azure OpenAI | Choose tools, compose a conversational response | Natural-language interface; it is **not** the source of financial calculations or inventory facts |
| Azure SQL | Read property records and save leads | Structured queries and parameterized SQL |
| Azure AI Search | Retrieve indexed textual knowledge | Retrieval results can ground a response; this public code does not create embeddings or use vector queries |
| Python mortgage service | Calculate repayment estimates | Formula-based, repeatable output with a financial disclaimer |
| FastAPI / Pydantic | Validate HTTP inputs and expose OpenAPI docs | Explicit typed request boundaries |
| Environment configuration | Load resource values outside Git | Keeps credentials out of the public repository |

## Runtime deployment reference

```mermaid
flowchart TB
    Browser["Browser / frontend"] --> Web["FastAPI container / App Service"]
    Web --> OpenAI["Azure OpenAI"]
    Web --> Search["Azure AI Search"]
    Web --> SQL[("Azure SQL Database")]
    Web -. "runtime settings" .-> Config["Environment variables / secret store"]
```

This is a **logical deployment reference**, not an assertion that this repository includes infrastructure-as-code or an automated Azure deployment.

## Important omissions in this public code

- No per-tenant `tenant_id` scoping or authorization enforcement.
- No ingestion pipeline, embeddings generation, vector/hybrid search, or persisted document index definitions.
- No multi-turn session storage or session quota enforcement.
- No authentication, rate limits, or complete audit logging for public endpoints.
- No infrastructure-as-code or GitHub Actions Azure CD workflow.

These are intentional distinctions between a public educational reference and a production application. Do not deploy the reference version directly as a public business API without implementing these controls.
