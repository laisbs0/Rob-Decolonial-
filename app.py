# Importando as bibliotecas
import gspread
import telegram
import os
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
TELEGRAM_TOKEN_BOT = os.environ["TELEGRAM_TOKEN_BOT"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"] #Conteúdo do arquivo .json
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U")
sheet = planilha.worksheet("País")
log = planilha.worksheet("chat")

app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> | <a href="/mapa">Mapa das Invasões</a>
<br>
"""

#Página inicial da aplicação
@app.route("/")
def index():
  return menu + "Olá mundo! Esse é meu site."

#Página sobre
@app.route("/sobre")
def sobre():
  return menu + "Meu nome é Lais e estou aprendendo a programar em Python."

#Página de contato
@app.route("/contato")
def contato():
  return menu + "laisbatistasantana@gmail.com"

#Rota para receber as atualizações do bot do Telegram
#Criei um Bot do Telegram que avisa se o país enviado pelo usuário já foi ou não invadido pela Inglaterra. O código a seguir é a rota criada para ser processada pelo Render e automatizar o robô. Contudo, o bot não funciona como deveria e segue enviando a mesma mensagem o tempo todo, independente da mensagem do usuário. Devolva o código corrigido.
# Importando as bibliotecas
import gspread
import telegram
import os
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
TELEGRAM_TOKEN_BOT = os.environ["TELEGRAM_TOKEN_BOT"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"] #Conteúdo do arquivo .json
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U")
sheet = planilha.worksheet("País")
log = planilha.worksheet("chat")

app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> | <a href="/mapa">Mapa das Invasões</a>
<br>
"""

#Página inicial da aplicação
@app.route("/")
def index():
  return menu + "Olá mundo! Esse é meu site."

#Página sobre
@app.route("/sobre")
def sobre():
  return menu + "Meu nome é Lais e estou aprendendo a programar em Python."

#Página de contato
@app.route("/contato")
def contato():
  return menu + "laisbatistasantana@gmail.com"

#Rota para receber as atualizações do bot do Telegram
#Criei um Bot do Telegram que avisa se o país enviado pelo usuário já foi ou não invadido pela Inglaterra. O código a seguir é a rota criada para ser processada pelo Render e automatizar o robô. Contudo, o bot não funciona como deveria e segue enviando a mesma mensagem o tempo todo, independente da mensagem do usuário. Devolva o código corrigido.
@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]
    paises_nao_invadidos = sheets.col_values(1)

    if message == "/start":
        replies = ["Bem-vindo(a)! Aqui te ajudo a descobrir quais países foram e não foram invadidos pela Inglaterra. Qual você quer saber?"]
    elif message in paises_nao_invadidos:
        replies = ["O país " + message + " nunca foi invadido pela Inglaterra."]
    else:
        replies = ["Isso aí já foi invadido pela Inglaterra. Haha. (☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)"]

    if message != "/start":
        replies.append("Pergunte sobre outro país")

    for reply in replies:
      nova_mensagem = {"chat_id": chat_id, "text": reply}
      requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN_BOT}/sendMessage", data=nova_mensagem)
        
#Página do mapinha que vou criar
@app.route("/mapa")
def mapa():
  return menu + "oi"

