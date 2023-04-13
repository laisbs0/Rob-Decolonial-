# Importando as bibliotecas
import gspread
import pandas as pd 
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
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
sheet = planilha.worksheet("países")
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
@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  paises_nao_invadidos = sheet.get_all_records()
  jorge = True

  if message == "/start":
    reply = "Bem-vindo(a)! Aqui te ajudo a descobrir quais países foram e não foram invadidos pela Inglaterra. Qual você quer saber?"
    message = update["message"]["text"]

  while jorge: 
    if message in paises_nao_invadidos:
      reply = "O país " + message + " nunca foi invadido pela Inglaterra."
    else:
      reply = "Isso aí já foi invadido pela Inglaterra. Haha. (☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)"

    nova_mensagem = {"chat_id": chat_id, "text": reply}
    requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN_BOT}/sendMessage", data=nova_mensagem)
    time.sleep(10)

    pergunta2 = "Pergunte sobre outro país"
    requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN_BOT}/sendMessage", data=pergunta2)
    time.sleep(10)
    message = update["message"]["text"]

    if message == " ":
      jorge = False

  mensagens.append([datahora, "enviada", username, first_name, chat_id, texto_resposta,])
  log.append_rows(mensagens)
  log.update("A1", update_id)


#Página do mapinha
@app.route("/mapa")
def mapa():
  return menu + "oi"
