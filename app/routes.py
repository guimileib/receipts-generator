from io import BytesIO
from flask import Blueprint, request, render_template, redirect, session, flash, send_file
from . import db
from app.clientes import Cliente
import os
from functools import wraps
from dotenv import load_dotenv
from .pdf import gerar_pdf
from .mail import enviar_email
import pandas as pd



main = Blueprint('main', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

def login_required(f):
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Você precisa fazer login primeiro', 'warning') # Mensagem de alerta
            return redirect('/login') 
        return f(*args, **kwargs) # Executa a função original
    return decorated_function

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        load_dotenv()

        if username == os.getenv('USER') and os.getenv('PASSWORD') == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login efetuado com sucesso!', 'success')
            return redirect('/clientes')
        else:
            flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('login.html')

# Rota protegida (painel de controle)
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session['username'])

# Logout
@main.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da conta!', 'info')
    return redirect('/login')

@main.route('/register', methods=['GET'])
@login_required
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
@login_required
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

#Simulando importação de dados
clientes = [
    {"nome": "João Silva", "email": "joao@email.com", "telefone": "123456789", "valor_servico": 150.00},
    {"nome": "Maria Souza", "email": "maria@email.com", "telefone": "987654321", "valor_servico": 200.00}
]


@main.route('/exportar')
def exportar():
    clientes = Cliente.query.all()
    clientes_lista = [{
        'Nome': cliente.nome,
        'Email': cliente.email,
        'Telefone': cliente.telefone,
        'Descrição do Serviço': cliente.descricao_servico,
        'Valor do Serviço': cliente.valor_servico,
        'Data de Cadastro': cliente.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')
    } for cliente in clientes]
    df = pd.DataFrame(clientes)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name='clientes.xlsx', as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")