# API examples

Start the API locally: `uvicorn app.main:app --reload`.

The interactive API reference is at `http://127.0.0.1:8000/docs`.

## Health — no credentials required

```bash
curl http://127.0.0.1:8000/health
```

## Mortgage estimate — no credentials required

```bash
curl -X POST http://127.0.0.1:8000/mortgage \
  -H "Content-Type: application/json" \
  -d '{"property_price_aed":1500000,"down_payment_percent":20,"annual_interest_rate":4.5,"tenure_years":25}'
```

Returns the estimated loan amount, monthly payment, and a disclaimer. It is not a bank offer.

## Property search — Azure SQL required

```bash
curl -X POST http://127.0.0.1:8000/search-properties \
  -H "Content-Type: application/json" \
  -d '{"area":"Dubai Marina","bedrooms":2,"max_price_aed":2500000}'
```

Requires your own populated Azure SQL database, configured ODBC Driver 18, and the schema expected by `app/services/database.py`.

## Knowledge search — Azure AI Search required

```bash
curl -X POST http://127.0.0.1:8000/knowledge-context \
  -H "Content-Type: application/json" \
  -d '{"question":"What amenities are available?","top_k":3}'
```

Requires your own index with the fields selected by `app/services/search.py`. This public implementation uses text retrieval; it does **not** create the index or embed documents.

## Chat — Azure OpenAI required

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"demo-session-1234","message":"Help me explore two-bedroom homes."}'
```

The `session_id` is echoed in the response; this public sample does not persist conversations. Tool calls that use SQL or Search also require those Azure services.

## Consent-based lead capture — Azure SQL required

Send `POST /leads` with a `LeadRequest` payload, including `consent: true`. **Do not send real personal data to an untrusted demo environment.**
