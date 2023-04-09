import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask
from tchan import ChannelScraper
import os
import requests

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1ZDyxhXlCtCjMbyKvYmMt_8jAKN5JSoZ7x3MqlnoyzAM")
sheet = planilha.worksheet("Sheet1")
api = gspread.authorize(conta)
planilha = api.open_by_key("11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U")
sheetpais = planilha.worksheet ("Página1")
sheet= planilha.worksheet ("chat")

app = Flask(__name__)

@app.route("/")
def hello_world():
   return "Olá, mundo!"

    
menu = """
<a href="/">Página inicial</a> | <a href="/invasoes">INVASÕES</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site."

@app.route("/sobre")
def sobre():
  return menu + "Meu nome é Lais e estou aprendendo a programar em Python."

@app.route("/contato")
def contato():
  return menu + "laisbatistasantana@gmail.com"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import os
    import requests
    import pandas as pd
    import datetime

    nome_json = "insper-automacao-lais-0029966cc57b.json"
    conta = ServiceAccountCredentials.from_json_keyfile_name(nome_json)

    GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
    with open("credenciais.json", mode="w") as arquivo:
        arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
    conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")

    token = os.environ.get('TELEGRAM_TOKEN_BOT')

    api = gspread.authorize(conta)
    planilha = api.open_by_key("11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U")
    sheetpais = planilha.worksheet ("Página1")
    sheet= planilha.worksheet ("chat")

    sheetpais.get("A1:Z1000")

    resposta = requests.get(f"https://api.telegram.org/bot{token}/getMe")
    print(resposta.json())

    resposta = requests.get(f"https://api.telegram.org/bot{token}/getUpdates")
    dados = resposta.json()["result"]
    print(f"Temos {len(dados)} novas atualizações:")
    print(dados)

    updates_processados = []

    import json
    print(json.dumps(dados, indent=2))

    updates_processados = []

    valor = 1675722349 # número de segundos desde 00/01/1970 00:00:00

    convertido = datetime.datetime.fromtimestamp(valor)

    paises = planilha.worksheet("Página1")
    paises = paises.get_all_records()
    df = pd.DataFrame(paises)
    df

    update_id = int(sheet.get("A1")[0][0])
    # Parâmetros de uma URL - também são chamados de query strings
    resposta = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?offset={update_id + 1}")
    dados = resposta.json()["result"]  
    print(f"Temos {len(dados)} novas atualizações:")
    mensagens = []
    for update in dados:
        update_id = update["update_id"]
        # Extrai dados para mostrar mensagem recebida
        first_name = update["message"]["from"]["first_name"]
        sender_id = update["message"]["from"]["id"]
        if "text" not in update["message"]:
            continue  # Essa mensagem não é um texto!
        message = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        datahora = str(datetime.datetime.fromtimestamp(update["message"]["date"]))
        if "username" in update["message"]["from"]:
            username = update["message"]["from"]["username"]
        else:
            username = "[não definido]"
        print(f"[{datahora}] Nova mensagem de {first_name} @{username} ({chat_id}): {message}")
        mensagens.append([datahora, "recebida", username, first_name, chat_id, message])
        # Define qual será a resposta e envia
        texto_resposta = " "
        print(message)

if message == "/start":
  texto_resposta = "Bem-vindo(a)! Aqui te ajudo a descobrir quais países foram e não foram invadidos pela Inglaterra. Qual você quer saber?"

elif message != " ":
  encontrou = False
  paises=df['localidade']
  for pais in paises:
    if pais == message: #permitir maiúsculas, minúsculas...
      encontrou = True
    if encontrou:
      texto_resposta = "Este país nunca foi invadido pela Inglaterra."
    else:
      texto_resposta = "Este país já foi invadido pela Inglaterra."

else:
  texto_resposta ="Obrigada por ter utilizado este canal, até mais!"

  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
  requests.post(f"https://api.telegram.org./bot{token}/sendMessage", data=nova_mensagem)
  mensagens.append([datahora, "enviada", username, first_name, chat_id, texto_resposta,])
# Atualiza planilha do sheets com último update processado
sheet.append_rows(mensagens)
sheet.update("A1", update_id)
