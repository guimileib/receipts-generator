from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Criado sem associar ao app ainda

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/clientes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco de dados com o app
    db.init_app(app)

    # Importa rotas e registra no app
    from .routes import main
    app.register_blueprint(main)

    # Cria as tabelas no banco se não existirem
    with app.app_context():
        db.create_all()

    return app