import logging
import os
from typing import Dict, List, Union, Optional
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import smtplib

class EmailTemplateProcessor:
    """
    HTML email template processor with dynamic macro replacement and file loading
    """
    def __init__(self, template_source: Optional[str] = None):
        """
        Initialize template processor
        
        :param template_source: HTML template string or file path
        """
        self._template = self._load_template(template_source) if template_source else ''
        self._macros = {}
    
    def _load_template(self, template_source: str) -> str:
        """
        Load template from file or use direct string
        
        :param template_source: Path to template file or template string
        :return: Processed HTML template content
        """
        # Check if source is a file path
        if os.path.isfile(template_source):
            try:
                with open(template_source, 'r', encoding='utf-8') as file:
                    return file.read()
            except IOError as e:
                logging.error(f"Error reading template file: {e}")
                return ''
        
        # If not a file, assume it's a direct template string
        return template_source
    
    def process(self, **kwargs) -> str:
        """
        Process the template with provided macro values
        
        :param kwargs: Macro key-value pairs
        :return: Processed HTML template
        """
        processed_template = self._template
        
        for macro, value in kwargs.items():
            processed_template = processed_template.replace(
                f'{{{{{macro}}}}}', 
                str(value)
            )
        
        return processed_template
    
    @classmethod
    def from_file(cls, file_path: str):
        """
        Class method to create template processor from a file
        
        :param file_path: Path to HTML template file
        :return: EmailTemplateProcessor instance
        """
        return cls(template_source=file_path)

class BrevoEmailService:
    """
    Enhanced email service with advanced template processing capabilities
    """
    def __init__(self, 
                 sender: Optional[str] = None, 
                 smtp_config: Optional[dict] = None,
                 template_dir: Optional[str] = None):
        """
        Initialize email service with optional configurations
        
        :param sender: Sender email address
        :param smtp_config: Custom SMTP configuration
        :param template_dir: Directory to load email templates from
        """
        self.logger = logging.getLogger(__name__)
        self.sender = sender or settings.DEFAULT_FROM_EMAIL
        self.smtp_config = smtp_config or {
            'host': settings.EMAIL_HOST,
            'port': settings.EMAIL_PORT,
            'username': settings.EMAIL_HOST_USER,
            'password': settings.EMAIL_HOST_PASSWORD,
            'use_tls': settings.EMAIL_USE_TLS
        }
        
        # Template directory for easy template loading
        self.template_dir = template_dir or os.path.join(settings.BASE_DIR, 'templates', 'emails')
        
        # HTML Templates storage
        self.templates: Dict[str, EmailTemplateProcessor] = {}
    
    def register_template(self, name: str, template_source: str):
        """
        Register an HTML email template from file or string
        
        :param name: Template identifier
        :param template_source: Path to template file or template string
        """
        # If it's a relative path, join with template directory
        if not os.path.isabs(template_source):
            template_source = os.path.join(self.template_dir, template_source)
        
        self.templates[name] = EmailTemplateProcessor(template_source)
    
    def send_template_email(
        self, 
        template_name: str, 
        subject: str, 
        recipients: Union[str, List[str]], 
        template_context: Optional[Dict] = None,
        plain_text_message: Optional[str] = None
    ) -> bool:
        """
        Send an email using a registered HTML template
        
        :param template_name: Name of the registered template
        :param subject: Email subject
        :param recipients: Email recipient(s)
        :param template_context: Context data for template rendering
        :param plain_text_message: Optional plain text alternative
        :return: Boolean indicating email send success
        """
        # Validate template exists
        if template_name not in self.templates:
            self.logger.error(f"Template '{template_name}' not found")
            return False
        
        # Process template
        template = self.templates[template_name]
        template_context = template_context or {}
        html_message = template.process(**template_context)
        
        # Normalize recipients
        if isinstance(recipients, str):
            recipients = [recipients]
        
        try:
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_text_message or 'View in HTML',
                from_email=self.sender,
                to=recipients
            )
            
            # Attach HTML alternative
            email.attach_alternative(html_message, "text/html")
            
            # Send email
            result = email.send()
            
            self.logger.info(f"Email sent to {recipients}")
            return result > 0
        
        except smtplib.SMTPException as smtp_error:
            self.logger.error(f"SMTP Error: {smtp_error}")
            return False
        except Exception as e:
            self.logger.error(f"Email sending failed: {e}")
            return False

email_service = BrevoEmailService()
email_service.register_template('login', 'login_request.html')

# Example usage

# # Register template from file
# email_service.register_template('login', 'login_request.html')

# # Send email with template
# result = email_service.send_template_email(
#     template_name='login',
#     subject='Your Login Details',
#     recipients=user.email,
#     template_context={
#         'first_name': user.first_name,
#     }
# )