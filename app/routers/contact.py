import uuid
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr

from app.models.emailSender import EmailSender
from app.models.googleSheetsManager import GoogleSheetsManager
from app.models.recaptchaManager import RecaptchaManager

router = APIRouter()

emailSender = EmailSender()
sheetManager = GoogleSheetsManager()
recaptchaManager = RecaptchaManager()

class RecaptchaRequest(BaseModel):
    """
    Model for contact message data received in the request.

    Attributes:
    - token (str): reCAPTCHA token for validation.
    - action (str): reCAPTCHA action, used for context in the assessment.
    - firstName (Optional[str]): Sender's first name.
    - lastName (Optional[str]): Sender's last name.
    - email (Optional[EmailStr]): Sender's email address.
    - phone (Optional[str]): Sender's phone number.
    - message (Optional[str]): Contact message from the sender.
    """
    token: str
    action: str
    firstName: str | None = None
    lastName: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    message: str | None = None

@router.post("/contact-message", summary="Receive and process a contact message")
async def recieve_contact_message(request: Request, recaptcha_request: RecaptchaRequest):
    """
    Endpoint to receive and process a contact message, including reCAPTCHA validation.

    This endpoint validates the request using reCAPTCHA. If validation is successful,
    it saves the information in a Google Sheets document and sends notification emails
    to both the admin and the sender.

    Parameters:
    - request (Request): The request object to obtain client IP and User-Agent.
    - recaptcha_request (RecaptchaRequest): Contact data sent by the client.

    Returns:
    - dict: Confirmation message on success or error detail on failure.
    
    Raises:
    - HTTPException 400: If the reCAPTCHA score is low, indicating potential risk.
    - HTTPException 500: If there is an error in reCAPTCHA validation or email notifications.
    """
    try:
        assessment_response = recaptchaManager.create_assessment(
            token=recaptcha_request.token,
            recaptcha_action=recaptcha_request.action,
            user_ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            ja3=None
        )
        score = assessment_response.risk_analysis.score
        reasons = assessment_response.risk_analysis.reasons

        if score >= 0.6:
            id = str(uuid.uuid4())
            sheetManager.save_contact_info(recaptcha_request, id)
            mail_data: dict = {
                "id": {id},
                "firstName": {recaptcha_request.firstName},
                "lastName": {recaptcha_request.lastName},
                "email": {recaptcha_request.email},
                "phone": {recaptcha_request.phone},
                "message": {recaptcha_request.message},
            }
            await emailSender.send_admin_notification(mail_data=mail_data)
            await emailSender.send_user_confirmation(recaptcha_request.email)
            
            return {
                "message": f"reCAPTCHA successfully validated. A confirmation email has been sent to {recaptcha_request.email}.",
                "score": score,
                "reasons": reasons
            }
        else:
            raise HTTPException(status_code=400, detail="Low reCAPTCHA score; potential risk detected.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in reCAPTCHA verification: {str(e)}")
