from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import os

def gerar_pdf(cliente):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Definindo a cor de fundo (azul escuro #39468f)
    c.setFillColorRGB(57/255, 70/255, 143/255)
    c.rect(0, 0, 612, 792, fill=1)  # Preenche a página inteira com a cor de fundo

    # Cabeçalho com logo e título
    c.setFillColor(colors.white)
    image_path = os.path.join(os.getcwd(), 'app', 'static', 'images', 'logo.png')
    if os.path.exists(image_path):
        c.drawImage(image_path, 40, 720, width=120, height=70)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(200, 750, "NOTA FISCAL DE SERVIÇO")
    c.setFont("Helvetica", 12)

    # Caixa branca para as informações do cliente
    c.setFillColor(colors.white)
    c.rect(40, 600, 530, 120, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 700, f"Cliente: {cliente.nome}")
    c.drawString(50, 680, f"Email: {cliente.email}")
    c.drawString(50, 660, f"Telefone: {cliente.telefone}")

    # Informações do serviço
    c.setFont("Helvetica", 12)
    c.drawString(50, 640, f"Descrição do Serviço:")
    c.drawString(50, 620, f"{cliente.descricao_servico}")
    c.drawString(50, 600, f"Valor do Serviço: R$ {cliente.valor_servico:.2f}")
    c.drawString(50, 580, f"Data de Cadastro: {cliente.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')}")

    # Rodapé
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Obrigado por confiar em nossos serviços!")
    c.drawString(50, 35, "Para mais informações, entre em contato: contato@viladosol.com")

    # Linha decorativa no rodapé
    c.setLineWidth(2)
    c.setStrokeColor(colors.white)
    c.line(50, 65, 550, 65)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
