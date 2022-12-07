from fpdf import FPDF
from datetime import datetime
import requests
# utilizado para tratar a imagem
import base64
import re
import os
from PIL import Image
from io import BytesIO
''' endereços do endpoint '''
urlApiProdutos = "http://localhost:8000/produto/"
headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}
class PDF(FPDF):
	def header(self):
		self.image("static/daTeusPulos.png", 5, 3, 10)
		self.set_font('helvetica', 'B', 15)
		self.cell(0, 5, 'Abc Bolinhas', 0, 1, 'C', 0)
		self.ln(5)
	def footer(self):
		self.set_y(-15)
		self.set_font('helvetica', 'I', 8)
		self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
	def listaTodos(self):
	
		pdf = PDF(orientation="P", unit="mm", format="A4") # L paisagem, P retrato
		pdf.set_author("Camilly")
		pdf.set_title('Produtos')
		pdf.alias_nb_pages() # mostra o número da página no rodapé
		pdf.add_page()
		# mostra o cabeçalho
		pdf.set_font('helvetica', 'b', 12)
		pdf.cell(190, 5, 'Produtos', 0, 1, 'C', 0)
		pdf.set_font('helvetica', '', 6)
		pdf.cell(190, 4, "Emitido em: " + str(datetime.now()), 0, 1, 'R')
		pdf.ln(5)
		# monta tabela para mostrar os dados
		pdf.set_font('helvetica', 'B', 8)
		pdf.cell(10, 5, 'ID', 0, 0, 'L')
		pdf.cell(50, 5, 'Produto', 0, 0, 'L')
		pdf.cell(65, 5, 'Descrição', 0, 0, 'L')
		pdf.cell(15, 5, 'Valor', 0, 0, 'L')
		pdf.cell(50, 5, 'Imagem', 0, 1, 'L')
		# busca na API e mostra todos os produtos
		pdf.set_font('helvetica', '', 8)
		try:
			response = requests.get(urlApiProdutos, headers=headers)
			result = response.json()
			if (response.status_code != 200):
				raise Exception(result[0])
			for row in result[0]:
				pdf.cell(10, 5, str(row['id_produto']), 0, 0, 'L')
				pdf.cell(50, 5, str(row['nome']),  0, 0, 'L')
				pdf.cell(65, 5, str(row['descricao']), 0, 0, 'L')
				pdf.cell(15, 5, str(row['valor_unitario']), 0, 0, 'L')
				# converte de string base64 para imagem
				img = Image.open(BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', row['foto']))))
				_auxNome = str(row['id_produto']) + '.png'
				img.save(_auxNome, "PNG")
				# posiciona e mostra no pdf a imagem
				pdf.image(_auxNome, pdf.get_x(), pdf.get_y(), 40)
				pdf.ln(40)
				# remove a imagem gerada
				os.remove(_auxNome)
		except Exception as e:
			print(e.args[0])
			pdf.multi_cell(190, 5, 'ERRO: ' + str(e.args[0]), 1, 'J', False)
		# baixa o relatório criado
		pdf.output('pdfProdutos.pdf')