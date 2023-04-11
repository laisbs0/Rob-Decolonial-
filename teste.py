
# Importando as bibliotecas
import gspread
import pandas as pd

# Pegando as credenciais
gc = gspread.service_account('credentialsLais.json')

# Dados da tabela
SHEET_ID = '11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U'
SHEET_NAME = 'Página1'
# Lendo a tabela
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Variavel a procurar
teste = "Andorra"

#Busca o dado da variável em toda a tabela
cell = worksheet.find(teste)

#imprime o resultado
print(worksheet.cell(cell.row, 2).value)
