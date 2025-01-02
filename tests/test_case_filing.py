import pytest
from src.pipelines.case_filing import CaseFilingPipeline
from src.services.email_service import EmailService
from src.models.case import Case, CaseStatus

@pytest.fixture
def email_service():
    return EmailService({
        "host": "localhost",
        "port": 587,
        "username": "test@lexarb.io",
        "password": "test"
    })

@pytest.fixture
def pipeline(email_service):
    return CaseFilingPipeline(email_service)

@pytest.mark.asyncio
async def test_case_filing_pipeline(pipeline):
    # Test data
    claimant = "claimant@example.com"
    respondent = "respondent@example.com"
    description = "Test case"
    
    # Process case
    case = await pipeline.process(claimant, respondent, description)
    
    # Verify case
    assert isinstance(case, Case)
    assert case.claimant == claimant
    assert case.respondent == respondent
    assert case.description == description
    assert case.status == CaseStatus.NEW
    assert case.case_number.startswith("ARB-")
    assert case.case_email.endswith("@lexarb.io")