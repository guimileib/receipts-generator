# Management Center: Receipts-Generator
Este projeto é uma aplicação web desenvolvida com Flask que permite gerar contratos personalizados para freelancers. 
Através de um formulário, o usuário insere os dados necessários, e o sistema gera um documento .docx com as informações preenchidas.

## Funcionalidades
- Autenticação de usuário com sessão segura.
- Formulário para inserção de dados do contrato.
- Geração de contrato em formato .docx com os dados fornecidos.
- Download automático do contrato gerado.
- Cadastro e listagem de clientes.
- Exportação de dados de clientes para Excel.
- Envio de contratos por e-mail (PDF).

### Como fazer o login?
Configure as variáveis de ambiente criando um arquivo .env na raiz do projeto:
```
USER=seu_usuario
PASSWORD=sua_senha
SECRET_KEY=sua_chave_secreta
```
### Como gerar os contratos?
Coloque o arquivo *contrato_modelo.docx* na pasta **static/doc/** (você vai precisar criar um folder doc e colocar o modelo de contrato dentro da pasta).


