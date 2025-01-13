from flask_mail import Message
from . import mail

def enviar_email(cliente, pdf_buffer):
    msg = Message("Nota Fiscal", sender="seuemail@gmail.com", recipients=[cliente.email])
    msg.body = f"Olá {cliente.nome},\n\nSegue em anexo a nota fiscal referente ao serviço prestado.\n\nAtenciosamente,\nEquipe Vila do Sol"
    msg.attach("nota_fiscal.pdf", "application/pdf", pdf_buffer.read())
    mail.send(msg)
