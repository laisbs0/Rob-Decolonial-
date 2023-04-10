@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]

    sheet.get("A1:Z1000")

    resposta = requests.get(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/getMe")
    print(resposta.json())

    resposta = requests.get(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/getUpdates")
    dados = resposta.json()["result"]
    print(f"Temos {len(dados)} novas atualizações:")
    print(dados)

    updates_processados = []

    import json

    print(json.dumps(dados, indent=2))

    updates_processados = []

    valor = datetime.datetime.now().timestamp()

    convertido = datetime.datetime.fromtimestamp(valor)

    paises = planilha.worksheet("Página1")
    paisesdf = paises.get_all_records()
    df = pd.DataFrame(paisesdf)

    update_id = int(sheet.get("A1")[0][0])

    # Parâmetros de uma URL - também são chamados de query strings
    resposta = requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/getUpdates?offset={update_id + 1}"
    )
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
    paises = df['localidade']
    for pais in paises:
        if pais == message:
            encontrou = True
            break
    if encontrou:
        texto_resposta = "Este país nunca foi invadido pela Inglaterra."
    else: 
        texto_resposta = "Este país já foi invadido pela Inglaterra."
    
nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
mensagens.append([datahora, "enviada", username, first_name, chat_id, texto_resposta])
