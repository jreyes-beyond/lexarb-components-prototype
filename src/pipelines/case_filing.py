import uuid
from typing import Optional
from ..models.case import Case, CaseStatus
from ..services.email_service import EmailService
from .base import Pipeline

class CaseFilingPipeline(Pipeline):
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    def _generate_case_number(self) -> str:
        """Generate a unique case number"""
        return f"ARB-{uuid.uuid4().hex[:8].upper()}"
    
    def _generate_case_email(self, case_number: str) -> str:
        """Generate a unique email for the case"""
        return f"{case_number.lower()}@lexarb.io"
    
    async def process(self, claimant: str, respondent: str, description: Optional[str] = None) -> Case:
        """Process a new case filing"""
        # Generate case details
        case_number = self._generate_case_number()
        case_email = self._generate_case_email(case_number)
        
        # Create case
        case = Case(
            case_number=case_number,
            case_email=case_email,
            claimant=claimant,
            respondent=respondent,
            description=description
        )
        
        # Set up email forwarding
        email_setup = await self.email_service.setup_case_email(case_email)
        if not email_setup:
            raise Exception("Failed to set up case email")
        
        # Send confirmation emails
        confirmation_content = f"Case {case_number} has been created. Please use {case_email} for all communications."
        for recipient in [claimant, respondent]:
            await self.email_service.send_email(
                recipient,
                f"Case {case_number} Created",
                confirmation_content
            )
        
        return case