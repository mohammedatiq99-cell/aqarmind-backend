from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.guardrails import public_safe_error_message, validate_user_message
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    KnowledgeRequest,
    LeadRequest,
    MortgageRequest,
    PropertySearchRequest,
)
from app.services.ai import ai_is_configured, generate_chat_answer
from app.services.database import (
    database_is_configured,
    list_properties,
    save_lead,
    search_properties,
)
from app.services.mortgage import calculate_mortgage
from app.services.search import retrieve_knowledge, search_is_configured

router = APIRouter()


@router.get("/")
def root():
    return {
        "service": "Aqarmind API",
        "description": "Public portfolio backend for an AI-powered real estate advisory platform.",
    }


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/config-check")
def config_check():
    # Deliberately returns readiness booleans only—never secret values.
    return {
        "ai_configured": ai_is_configured(),
        "search_configured": search_is_configured(),
        "database_configured": database_is_configured(),
    }


@router.get("/properties")
def properties():
    try:
        return {"items": list_properties()}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=public_safe_error_message()) from exc


@router.post("/search-properties")
def property_search(request: PropertySearchRequest):
    try:
        return {"items": search_properties(**request.model_dump())}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=public_safe_error_message()) from exc


@router.post("/mortgage")
def mortgage(request: MortgageRequest):
    return calculate_mortgage(**request.model_dump())


@router.post("/knowledge-context")
def knowledge_context(request: KnowledgeRequest):
    try:
        return {"items": retrieve_knowledge(request.question, request.top_k)}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=public_safe_error_message()) from exc


@router.post("/leads", status_code=status.HTTP_201_CREATED)
def capture_lead(request: LeadRequest):
    if not request.consent:
        raise HTTPException(status_code=422, detail="Consent is required.")

    try:
        save_lead(request.model_dump())
        return {"status": "accepted"}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=public_safe_error_message()) from exc


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = validate_user_message(request.message)
    try:
        answer = generate_chat_answer(message)
        return ChatResponse(answer=answer, session_id=request.session_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=public_safe_error_message()) from exc
