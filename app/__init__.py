from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Criado sem associar ao app ainda

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)    # Inicializa o banco de dados com o app

    from .routes import main    # Importa rotas e registra no app
    app.register_blueprint(main)

    with app.app_context():     # Cria as tabelas no banco se não existirem
        db.create_all()

    return app