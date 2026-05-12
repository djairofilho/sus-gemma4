from enum import StrEnum

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EMERGENCY = "emergency"


class Referral(StrEnum):
    UBS = "UBS"
    UPA = "UPA"
    SAMU = "SAMU"
    EMERGENCY = "emergency"
    SCHEDULED_FOLLOW_UP = "scheduled_follow_up"
    ADMINISTRATIVE_GUIDANCE = "administrative_guidance"
    UNKNOWN = "unknown"


class HealthResponse(BaseModel):
    status: str
    model_runtime: str
    rag_index: str


class TriageRequest(BaseModel):
    case_text: str = Field(min_length=3, max_length=4000)


class TriageResponse(BaseModel):
    risk_level: RiskLevel
    summary: str
    suggested_action: str
    referral: Referral
    red_flags: list[str]
    sus_basis: list[str]
    limitations: str
    safety_notice: str
    runtime: str = "mock"
