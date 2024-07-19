from docx2pdf import convert
import telebot
from TOKEN import TOKEN
import os

convert_bot = telebot.TeleBot(TOKEN)

@convert_bot.message_handler(commands=['start'])
def start_message(message):
    convert_bot.reply_to(message, "Отправляй мне ворд документ и получишь PDF")

@convert_bot.message_handler(content_types=['document'])
def conversion(message):
    file_info = convert_bot.get_file(message.document.file_id)
    downloaded_file = convert_bot.download_file(file_info.file_path)

    file_path = message.document.file_name
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    pdf_path = file_path.replace('.docx', '.pdf')
    convert(file_path, pdf_path)

    with open(pdf_path, 'rb') as pdf_file:
        convert_bot.send_document(message.chat.id, pdf_file)

    os.remove(file_path)
    os.remove(pdf_path)

convert_bot.polling()
