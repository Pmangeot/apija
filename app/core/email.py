import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape
from core.config import settings 

class EmailSender:
    def __init__(self, template_dir: str = "templates"):
        # Récupération des configurations SMTP depuis settings
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        
        # Configuration du moteur de template Jinja2
        self.template_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def send_email(self, to_email: str, subject: str, template_name: str, context: dict):
        try:
            # Chargement et rendu du template
            template = self.template_env.get_template(template_name)
            html_content = template.render(context)

            # Création du message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject

            # Ajout du corps du message au format HTML
            msg.attach(MIMEText(html_content, 'html'))

            # Connexion et envoi via SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Activer TLS
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()

        except Exception as e:
            raise Exception(f"Erreur lors de l'envoi de l'email: {str(e)}")
