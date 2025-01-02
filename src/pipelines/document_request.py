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
    
    async def process_document_response(
        self,
        case_id: UUID,
        email_content: str,
        attachments: List[tuple]  # List of (filename, content_bytes)
    ) -> List[Document]:
        """Process incoming document response email"""
        documents = []
        
        for filename, content in attachments:
            # Save document
            filepath = await self.document_processor.save_document(content, filename)
            
            # Extract metadata
            metadata = await self.document_processor.extract_metadata(filepath)
            
            # Create document record
            document = Document(
                case_id=case_id,
                filename=filename,
                content_type=self._get_content_type(filename),
                size=len(content),
                document_type=self._infer_document_type(filename, email_content),
                metadata=metadata
            )
            
            documents.append(document)
        
        return documents
    
    def _get_content_type(self, filename: str) -> str:
        """Infer content type from filename"""
        ext = Path(filename).suffix.lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    def _infer_document_type(self, filename: str, email_content: str) -> DocumentType:
        """Infer document type from filename and email content"""
        filename_lower = filename.lower()
        email_lower = email_content.lower()
        
        # Check filename and email content for keywords
        if any(word in filename_lower or word in email_lower 
               for word in ['evidence', 'exhibit', 'proof']):
            return DocumentType.EVIDENCE
        elif any(word in filename_lower or word in email_lower 
                for word in ['plead', 'motion', 'petition']):
            return DocumentType.PLEADING
        elif any(word in filename_lower or word in email_lower 
                for word in ['letter', 'correspondence', 'communication']):
            return DocumentType.CORRESPONDENCE
        elif any(word in filename_lower or word in email_lower 
                for word in ['award', 'decision', 'judgment']):
            return DocumentType.AWARD
        
        return DocumentType.OTHER