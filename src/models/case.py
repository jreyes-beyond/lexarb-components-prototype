from .base import BaseDBModel
from pydantic import EmailStr
from typing import Optional
from enum import Enum

class CaseStatus(str, Enum):
    NEW = "new"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"

class Case(BaseDBModel):
    case_number: str
    case_email: EmailStr
    claimant: str
    respondent: str
    status: CaseStatus = CaseStatus.NEW
    description: Optional[str] = None