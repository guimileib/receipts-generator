from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    print(f"Cliente: {nome}, Email: {email}, Telefone: {telefone}")

if __name__ == '__main__':
    app.run(debug=True)