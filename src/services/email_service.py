import aiosmtplib
from email.message import EmailMessage
from typing import Optional

class EmailService:
    def __init__(self, smtp_config: dict):
        self.config = smtp_config
    
    async def setup_case_email(self, case_email: str) -> bool:
        """Set up email forwarding for a case"""
        # In prototype, just simulate email setup
        print(f"Setting up email forwarding for {case_email}")
        return True
    
    async def send_email(self, to_email: str, subject: str, content: str) -> bool:
        """Send an email"""
        try:
            message = EmailMessage()
            message["From"] = self.config["username"]
            message["To"] = to_email
            message["Subject"] = subject
            message.set_content(content)
            
            async with aiosmtplib.SMTP(
                hostname=self.config["host"],
                port=self.config["port"],
                use_tls=True
            ) as smtp:
                await smtp.send_message(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False