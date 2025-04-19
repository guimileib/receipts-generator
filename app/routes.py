from io import BytesIO
import os
from functools import wraps

from flask import Blueprint, request, render_template, redirect, session, flash, send_file, url_for
from dotenv import load_dotenv
import pandas as pd
from docx import Document

from . import db
from app.clientes import Cliente
from .pdf import gerar_pdf
from .mail import enviar_email

main = Blueprint('main', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

def login_required(f):
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Você precisa fazer login primeiro', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        load_dotenv()

        if username == os.getenv('USER') and password == os.getenv('PASSWORD'):
            session['logged_in'] = True
            session['username'] = username
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuário ou senha inválidos', 'danger')
            return redirect(url_for('main.login'))
    
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da conta!', 'info')
    return redirect(url_for('main.login'))

@main.route('/contrato', methods=['GET'])
@login_required
def show_register_form_contract():
    return render_template('contrato.html')
    
@main.route('/gerar_contrato', methods=['POST'])
@login_required
def gerar_contrato():
    nome_func = request.form['nome_func']
    servico = request.form['servico']
    valor = request.form['valor']
    endereco = request.form['endereco']
    data = request.form['data']

    # Usar caminho absoluto para o modelo de contrato
    caminho_modelo = os.path.join(os.getcwd(), "doc", "contrato_modelo.docx")
    
    try:
        doc = Document(caminho_modelo)

        for paragrafo in doc.paragraphs:
            paragrafo.text = paragrafo.text.replace("{nome_func}", nome_func)
            paragrafo.text = paragrafo.text.replace("{servico}", servico)
            paragrafo.text = paragrafo.text.replace("{valor}", valor)
            paragrafo.text = paragrafo.text.replace("{endereco}", endereco)
            paragrafo.text = paragrafo.text.replace("{data}", data)

        # Salvar em um BytesIO para não precisar criar arquivo temporário
        output = BytesIO()
        doc.save(output)
        output.seek(0)

        nome_arquivo = f"contrato_{nome_func.replace(' ', '_')}.docx"
        
        # Retornar o arquivo diretamente da memória
        return send_file(
            output,
            as_attachment=True,
            download_name=nome_arquivo,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        flash(f'Erro ao gerar contrato: {str(e)}', 'danger')
        return redirect(url_for('main.show_register_form_contract'))

@main.route('/register', methods=['GET'])
@login_required
def show_register_form():
    return render_template('register.html')

@main.route('/register', methods=['POST'])
@login_required
def register():
    try:
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        valor_servico = float(request.form['service_value'])
        descricao_servico = request.form['service_description']

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

        # Gerar PDF e enviar email
        pdf_buffer = gerar_pdf(novo_cliente)
        enviar_email(novo_cliente, pdf_buffer)
        
        flash('Cliente cadastrado e e-mail enviado!', 'success')
        return redirect(url_for('main.listar_clientes'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar cliente: {str(e)}', 'danger')
        return redirect(url_for('main.show_register_form'))

@main.route('/clientes')
@login_required
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@main.route('/exportar')
@login_required
def exportar():
    try:
        clientes = Cliente.query.all()
        clientes_lista = [{
            'Nome': cliente.nome,
            'Email': cliente.email,
            'Telefone': cliente.telefone,
            'Descrição do Serviço': cliente.descricao_servico,
            'Valor do Serviço': cliente.valor_servico,
            'Endereço': cliente.endereco
        } for cliente in clientes]

        df = pd.DataFrame(clientes_lista)
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        output.seek(0)
        
        return send_file(
            output, 
            download_name='clientes.xlsx', 
            as_attachment=True, 
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        flash(f'Erro ao exportar dados: {str(e)}', 'danger')
        return redirect(url_for('main.listar_clientes'))