from fastapi import BackgroundTasks, APIRouter
from core.email import EmailSender

# Instanciation d'EmailSender
email_sender = EmailSender()

router = APIRouter()

@router.post("/send")
async def send_email_endpoint(background_tasks: BackgroundTasks, to_email: str, subject: str, title: str, content: str):
    # Contexte à passer au template
    context = {
        "subject": subject,
        "title": title,
        "content": content,
        "sender_name": "Your Company"
    }

    # Envoi de l'email en arrière-plan
    background_tasks.add_task(email_sender.send_email, to_email, subject, "email_template.html", context)
    return {"message": "Email en cours d'envoi"}