import smtplib
import os
from email.message import EmailMessage

def enviarEmailBoasVindas(emailDestino: str, nomeUsuario: str):
    remetenteEmail = os.getenv("EMAIL_REMETENTE")
    senhaEmail = os.getenv("EMAIL_SENHA")

    if not remetenteEmail or not senhaEmail:
        print("Credenciais de email nao configuradas no .env")
        return

    mensagemEmail = EmailMessage()
    mensagemEmail["Subject"] = "Bem-vindo(a) ao Sistema da Farmacia!"
    mensagemEmail["From"] = remetenteEmail
    mensagemEmail["To"] = emailDestino

    conteudoHtml = f"""
    <html>
        <body>
            <h2>Ola, {nomeUsuario}!</h2>
            <p>O seu cadastro no <strong>Sistema da Farmacia</strong> foi realizado com sucesso.</p>
            <p>Estamos felizes em ter voce conosco.</p>
        </body>
    </html>
    """
    mensagemEmail.add_alternative(conteudoHtml, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidorSmtp:
            servidorSmtp.ehlo()
            servidorSmtp.starttls()
            servidorSmtp.ehlo()
            servidorSmtp.login(remetenteEmail, senhaEmail)
            servidorSmtp.send_message(mensagemEmail)
            print("Email enviado com sucesso.")
    except Exception as erroDisparo:
        print(f"Erro ao enviar email: {erroDisparo}")