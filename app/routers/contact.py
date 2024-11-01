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
    token: str
    action: str
    firstName: str | None = None
    lastName: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    message: str | None = None

@router.post("/verify-recaptcha")
async def verify_recaptcha(request: Request, recaptcha_request: RecaptchaRequest):
    
    try:
        # Llamamos a la función de evaluación
        assessment_response = recaptchaManager.create_assessment(
            token=recaptcha_request.token,
            recaptcha_action=recaptcha_request.action,
            user_ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            ja3=None
        )
        score = assessment_response.risk_analysis.score
        reasons = assessment_response.risk_analysis.reasons

        if score >= 0.7:  # Cambia este umbral según tu preferencia 
            sheetManager.save_contact_info(recaptcha_request)
            mail_data: dict = {
                "firstName": {recaptcha_request.firstName},
                "lastName": {recaptcha_request.lastName},
                "email": {recaptcha_request.email},
                "phone": {recaptcha_request.phone},
                "message": {recaptcha_request.message},
            }
            await emailSender.send_admin_notification(mail_data=mail_data)
            await emailSender.send_user_confirmation(recaptcha_request.email)
            
            return {"message": f"reCAPTCHA validado exitosamente. Se envió un mail de confirmación a {recaptcha_request.email}.", "score": score, "reasons": reasons}
        else:
            raise HTTPException(status_code=400, detail="El puntaje de reCAPTCHA es bajo; sospecha de riesgo")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la verificación de reCAPTCHA: {str(e)}")
