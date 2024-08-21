from fastapi import BackgroundTasks, APIRouter, Depends, HTTPException
from core.email import EmailSender
from core.security import get_current_user
from models.m_user import User

# Instanciation d'EmailSender
email_sender = EmailSender()

router = APIRouter()

@router.post("/send")
async def send_email_endpoint(background_tasks: BackgroundTasks, to_email: str, subject: str, title: str, content: str,  user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    context = {
        "subject": subject,
        "title": title,
        "content": content,
        "sender_name": "Your Company"
    }

    # Envoi de l'email en arrière-plan
    background_tasks.add_task(email_sender.send_email, to_email, subject, "email_template.html", context)
    return {"message": "Email en cours d'envoi"}