from json.decoder import JSONDecodeError
from telegram.ext import MessageHandler, CommandHandler, Filters, Updater
import data_interactions as di
import reply_markups as rm
import command_names
from commands import commands, weighted_sum, additional_criteria
import logging
import json


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет! Отправь мне csv файл с порядковыми данными", reply_markup=rm.reply_kb_markup)


def handle_message(update, context):
    text = update.message.text
    command = commands.get(text)
    if command:
        command(update, context)
    try:
        weights = json.loads(text)
    except JSONDecodeError:
        return
    weighted_sum(update, context, weights)


def handle_document(update, context):
    document = update.message.document
    file = bot.get_file(document.file_id)
    file_path = file.file_path
    caption = update.message.caption
    if caption:
        try:
            weights = json.loads(caption)
        except JSONDecodeError:
            return
        df = di.get_df_bypath(file_path)
        additional_criteria(update, context, df, weights)
    di.save_data(update.effective_chat.id, file_path)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Данные сохранены!", reply_markup=rm.reply_kb_markup)


def handle_error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Упс! Произошла ошибка")


updater = Updater(token='1729255835:AAEZvbzlEfRshR7IlfWbg_lPyxx0rqsrE2M', use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
start_handler = CommandHandler(command_names.start, start)
document_handler = MessageHandler(Filters.document, handle_document)
message_handler = MessageHandler(Filters.text, handle_message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(document_handler)
# dispatcher.add_error_handler(handle_error)

updater.start_polling()
