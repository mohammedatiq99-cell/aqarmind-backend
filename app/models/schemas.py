from pydantic import BaseModel, EmailStr, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=4, max_length=120)
    message: str


class ChatResponse(BaseModel):
    answer: str
    session_id: str


class PropertySearchRequest(BaseModel):
    area: str | None = None
    bedrooms: int | None = Field(default=None, ge=0, le=20)
    max_price_aed: float | None = Field(default=None, gt=0)
    property_type: str | None = None
    developer: str | None = None


class MortgageRequest(BaseModel):
    property_price_aed: float = Field(gt=0)
    down_payment_percent: float = Field(default=20, ge=0, lt=100)
    annual_interest_rate: float = Field(default=4.5, ge=0, le=30)
    tenure_years: int = Field(default=25, gt=0, le=40)


class LeadRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=40)
    budget_aed: float | None = Field(default=None, gt=0)
    preferred_area: str | None = Field(default=None, max_length=120)
    consent: bool
    session_id: str | None = Field(default=None, max_length=120)


class KnowledgeRequest(BaseModel):
    question: str = Field(min_length=2, max_length=6000)
    top_k: int = Field(default=5, ge=1, le=10)
