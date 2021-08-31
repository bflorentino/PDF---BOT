from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
import logging
import os
from pics2pdf import Pic2pdf

text = "Use /photopdf to make a pdf from pictures"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):

    context.bot.send_message(chat_id = update.effective_chat.id, 
                            text = text, 
                            parse_mode='MarkdownV2')


if __name__ == "__main__":

    updater = Updater(token = os.environ["TOKEN1"], use_context= True)
    dp = updater.dispatcher
    pictopdf = Pic2pdf()


    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(ConversationHandler(

        entry_points= [CommandHandler('photopdf', pictopdf.pictopdfCommandHandlder)],

        states= {pictopdf.getPicToPdfState(): [MessageHandler(Filters.photo, pictopdf.imputImgs)]},

        fallbacks=[]
    ))
    dp.add_handler(MessageHandler(Filters.regex(r"Cancel"),pictopdf.cancel))
    dp.add_handler(MessageHandler(Filters.regex(r"Convert to PDF"),pictopdf.conversionToPDF))


updater.start_polling()
updater.idle()