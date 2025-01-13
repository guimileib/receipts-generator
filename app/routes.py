from flask import Blueprint, request, jsonify, redirect, url_for
from . import db
from app.clientes import Cliente

main = Blueprint

@main.route('/')
def index():
    return "Bem-vindo ao sistema de cadastro de clientes!"

@main.route('/register', methods=['POST'])
def cadastrar():
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
    return jsonify(novo_cliente.to_dict())

@main.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes])
