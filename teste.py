
# Importando as bibliotecas
import gspread
import pandas as pd
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

#Dados do Google
# Pegando as credenciais
gc = gspread.service_account('credentialsLais.json')

# Dados da tabela
SHEET_ID = '11OkESzP3BYZqkuKGJM4sW4YvywJKNeA6lEr9ReQ3b0U'
SHEET_NAME = 'Página1'
# Lendo a tabela
spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Criando as Funções para o Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Executa comandos quando é enviado o comando /start
    user = update.effective_user # Pega o nome do usuário
    await update.message.reply_html(
        rf"Olá {user.mention_html()}! Informe um país",
        reply_markup=ForceReply(selective=True),
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Quando o usuário enviar uma mensagem
    pais = update.message.text # Armazena a mensagem
    # Verifica se o país informado foi invadido
    cell = worksheet.find(pais)
    if cell:
        await update.message.reply_text(pais + " " + worksheet.cell(cell.row, 2).value)
    else:
        await update.message.reply_text("Não conheço esse país")

def main() -> None:
    

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6143401120:AAGXla_sxuLlaBiHBBZmp_apFBkI6nhtd3Q").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot until the user presses Ctrl-C
    # application.run_polling()

if __name__ == "__main__":
    main()