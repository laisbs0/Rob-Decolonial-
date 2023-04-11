
# Importando as bibliotecas
import gspread
import pandas as pd # Acho que nem ta usando o pandas, talvez use la no Render, tem que testar
import Flask
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

app = Flask(__name__)
@app.route('/')
def testeRobo():

    """Dados do Google"""
    # Pegando as credenciais | Já ta com as suas, se quiser é só trocar o nome do json
    gc = gspread.service_account('credentialsLais.json') # Aqui e no GitHub também

    # Dados da tabela | Já ta usando os dados da sua
    SHEET_ID = '11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U'
    # Só se vc mudar esse nome horrível da tabela pq pelamor
    SHEET_NAME = 'Página1' # Aí troca aqui também
    # Lendo a tabela
    spreadsheet = gc.open_by_key(SHEET_ID) # Ta usando variavel mas pode por direto
    worksheet = spreadsheet.worksheet(SHEET_NAME) # Ta usando variavel mas pode por direto

    """Criando as Funções para o Telegram"""

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Executa comandos quando é enviado o comando /start
        user = update.effective_user # Pega o nome do usuário
        await update.message.reply_html(
            # Envia a primeira mensagem | Pode trocar ela, só que tem que ficar na mesma linha
            rf"Olá {user.mention_html()}! Informe um país",
            # A resposta do usuário vai vir como 'reply'
            reply_markup=ForceReply(selective=True),
        )

    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Quando o usuário enviar uma mensagem
        pais = update.message.text # Armazena a mensagem
        # Verifica se o país informado consta na tabela
        cell = worksheet.find(pais)
        if cell:# Verifica se a variável é verdadeira (não nula)
            # Responde com o valor da celula da coluna B
            await update.message.reply_text(pais + " " + worksheet.cell(cell.row, 2).value)
        else:# Se não, a variável não existe (nula)
            await update.message.reply_text("Não conheço esse país")

    """Inicia o Bot"""
    def main() -> None:
        # Cria a aplicação utilizando o token do Bot | Troca aqui pelo Token do seu <3
        application = Application.builder().token("6143401120:AAGXla_sxuLlaBiHBBZmp_apFBkI6nhtd3Q").build()

        # Cria o Handler para a função /Start | Da pra criar outros comandos também se vc quiser
        application.add_handler(CommandHandler("start", start))
        
        # Cria o Handler para as outras mensagens do usuário
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
    #Isso aqui eu n sei pra que serve, tava no exemplo lá e eu deixei ¯\_(ツ)_/¯
    #Parece ser uma tratativa de nome de função
    if __name__ == "__main__":
        main()