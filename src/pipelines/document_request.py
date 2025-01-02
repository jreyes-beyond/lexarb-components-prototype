from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pathlib import Path

from ..models.document import Document, DocumentType
from ..services.email_service import EmailService
from ..services.document_processor import DocumentProcessor
from .base import Pipeline

class DocumentRequestPipeline(Pipeline):
    def __init__(
        self,
        email_service: EmailService,
        document_processor: DocumentProcessor
    ):
        self.email_service = email_service
        self.document_processor = document_processor
    
    async def request_documents(
        self,
        case_id: UUID,
        recipient_email: str,
        document_types: List[DocumentType],
        deadline: datetime
    ) -> bool:
        """Send document request to recipient"""
        # Generate request content
        doc_types_str = ", ".join([dt.value for dt in document_types])
        deadline_str = deadline.strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""
        Document Request for Case {case_id}
        
        Please provide the following documents by {deadline_str}:
        - {doc_types_str}
        
        Please reply to this email with the requested documents attached.
        """
        
        # Send request email
        return await self.email_service.send_email(
            recipient_email,
            f"Document Request - Case {case_id}",
            content
        )
