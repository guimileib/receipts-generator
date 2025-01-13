from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv


db = SQLAlchemy()  # Criado sem associar ao app ainda
mail = Mail()

def create_app(config_filename=None):
    app = Flask(__name__,  instance_relative_config=True)

    load_dotenv()

    app.config.from_object('config')

    if config_filename:
        app.config.from_pyfile(config_filename, silent=True)
    else:
        app.config.from_pyfile('config.py')

    db.init_app(app)    # Inicializa o banco de dados com o app e mail
    mail.init_app(app)

    from .routes import main    # Importa rotas e registra no app
    app.register_blueprint(main)

    with app.app_context():     # Cria as tabelas no banco se não existirem
        db.create_all()

    return app