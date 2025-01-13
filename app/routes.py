from io import BytesIO
from flask import Blueprint, request, render_template, redirect
from . import db
from app.clientes import Cliente
import os
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas

main = Blueprint('main', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Flask-Mail configuração
main.config['MAIL_SERVER'] = 'smtp.gmail.com'  
main.config['MAIL_PORT'] = 465  # Porta de envio de e-mail (geralmente 465 ou 587)
main.config['MAIL_USERNAME'] = 'seuemail@gmail.com'
main.config['MAIL_PASSWORD'] = 'suasenha'
main.config['MAIL_USE_TLS'] = False
main.config['MAIL_USE_SSL'] = True
mail = Mail(main)


# Configuração do pdf que vai gerar o email
def gerar_pdf(cliente):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Nota Fiscal - Serviço Prestado para: {cliente.nome}")
    c.drawString(100, 730, f"Email: {cliente.email}")
    c.drawString(100, 710, f"Telefone: {cliente.telefone}")
    c.drawString(100, 690, f"Descrição do Serviço: {cliente.descricao_servico}")
    c.drawString(100, 670, f"Valor do Serviço: R$ {cliente.valor_servico:.2f}")
    c.drawString(100, 650, f"Data de Cadastro: {cliente.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')}")
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def enviar_email(cliente, pdf_buffer):
    msg = Message("Nota Fiscal", sender="seuemail@gmail.com", recipients=[cliente.email])
    msg.body = f"Olá {cliente.nome},\n\nSegue em anexo a nota fiscal referente ao serviço prestado.\n\nAtenciosamente,\nSeu Nome"
    msg.attach("nota_fiscal.pdf", "application/pdf", pdf_buffer.read())
    mail.send(msg)

@main.route('/')
def index():
    return "Bem-vindo ao sistema de cadastro de clientes!"

@main.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

@main.route('/register', methods=['POST'])
def register():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']

    valor_servico = float(request.form['service_value'])
    descricao_servico = request.form['service_description']
    print(f"Cliente: {nome}, Email: {email}, Telefone: {telefone}, Valor: R$ {valor_servico:.2f}, Serviço: {descricao_servico}, Endereço: {endereco}")

    novo_cliente = Cliente(
        nome=nome, 
        email=email, 
        telefone=telefone, 
        valor_servico=valor_servico, 
        descricao_servico=descricao_servico, 
        endereco=endereco
        )

    db.session.add(novo_cliente)
    db.session.commit()
    #return jsonify(novo_cliente.to_dict())
    return redirect('/clientes')

@main.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)
