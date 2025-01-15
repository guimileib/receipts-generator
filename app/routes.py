from io import BytesIO
from flask import Blueprint, request, render_template, redirect
from . import db
from app.clientes import Cliente
import os
from .pdf import gerar_pdf
from .mail import enviar_email

main = Blueprint('main', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@main.route("/")
def home():
    return render_template('register.html')

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

    pdf_buffer = gerar_pdf(novo_cliente)
    enviar_email(novo_cliente, pdf_buffer)
    return redirect('/clientes')

    

@main.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)
