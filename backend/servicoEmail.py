import smtplib
import os
from email.message import EmailMessage

def enviarEmailBoasVindas(emailDestino: str, nomeUsuario: str):
    remetenteEmail = os.getenv("EMAIL_REMETENTE")
    senhaEmail = os.getenv("EMAIL_SENHA")

    if not remetenteEmail or not senhaEmail:
        print("Credenciais de email não configuradas no .env")
        return

    mensagemEmail = EmailMessage()
    mensagemEmail["Subject"] = "Bem-vindo(a) ao Sistema da Farmácia!"
    mensagemEmail["From"] = remetenteEmail
    mensagemEmail["To"] = emailDestino

    conteudoHtml = f"""
    <html>
        <body>
            <h2>Olá, {nomeUsuario}!</h2>
            <p>O seu cadastro no <strong>Sistema da Farmácia</strong> foi realizado com sucesso.</p>
            <p>Estamos felizes em ter você conosco.</p>
        </body>
    </html>
    """
    mensagemEmail.add_alternative(conteudoHtml, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidorSmtp:
            servidorSmtp.login(remetenteEmail, senhaEmail)
            servidorSmtp.send_message(mensagemEmail)
    except Exception as erroDisparo:
        print(f"Erro ao enviar email: {erroDisparo}")