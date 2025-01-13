from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def gerar_pdf(cliente):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Nota Fiscal - Serviço Prestado para: {cliente.nome}")
    c.drawString(100, 730, f"Email: {cliente.email}")
    c.drawString(100, 710, f"Telefone: {cliente.telefone}")
    c.drawString(100, 690, f"Descrição do Serviço: {cliente.descricao_servico}")
    c.drawString(100, 670, f"Valor do Serviço: R$ {cliente.valor_servico:.2f}")
    c.drawString(100, 650, f"Data de Cadastro: {cliente.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')}")
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
