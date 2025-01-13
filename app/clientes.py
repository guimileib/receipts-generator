from . import db # importação deve ser de onde configurou o db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    valor_servico = db.Column(db.Float, nullable=False)
    descricao_servico = db.Column(db.String(120), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "valor_servico": self.valor_servico,
            "descricao_servico": self.descricao_servico
        }

