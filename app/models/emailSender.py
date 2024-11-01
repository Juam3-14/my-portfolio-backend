import os
import sendgrid
from sendgrid.helpers.mail import *

class EmailSender:
    def __init__(self):
        self.username=os.environ.get("MAIL_USERNAME")
        self.mail_sender=os.environ.get("MAIL_FROM")
        self.admin_email=os.environ.get("ADMIN_EMAIL")        
        
    async def send_admin_notification(self, mail_data: dict) -> None:
        message = Mail(
            from_email=Email(str(self.mail_sender)),
            to_emails=To(str(self.admin_email)),
            subject="Nuevo mensaje de contacto a tu portfolio personal",
            plain_text_content= Content("text/plain", f"""
                    Nombre: {mail_data.get("firstName", None)},
                    Apellido: {mail_data.get("lastName", None)},
                    Email: {mail_data.get("email", None)},
                    Teléfono: {mail_data.get("phone", None)},
                    Mensaje: {mail_data.get("message", None)}
            """)
        )
        try:
            sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.client.mail.send.post(request_body=message.get())
            return response
        except Exception as e:
            print(e)
        
    async def send_user_confirmation(self, email: str):
        message = Mail(
            from_email=Email(str(self.mail_sender)),
            to_emails=To(email),
            subject="Message confirmation - Juan Pablo Piemonte's personal portfolio",
            plain_text_content=Content("text/plain", "Thanks for your message! I'll be answering soon!")
        )
        try:
            sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            print(message.get())
            response = sg.client.mail.send.post(request_body=message.get())           
            return response
        except Exception as e:
            print(e)