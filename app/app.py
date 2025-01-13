from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db_models.clientes import Cliente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/database.db' # Especifica o camiho onde será salvo os dados
db = SQLAlchemy(app)

@app.route('/register', methods=['POST'])
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
    
    return redirect ('/')

@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

if __name__ == '__main__':
    app.run(debug=True)