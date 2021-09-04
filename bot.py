from PdfAppend import PdfAppend
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
import logging
import os
from pics2pdf import Pic2pdf


text = '''
Use /photopdf to make a pdf from pictures
Use /mergepdf to merge pdf files 
            '''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



def start(update, context):

    context.bot.send_message(chat_id = update.effective_chat.id, 
                            text = text, 
                            parse_mode='MarkdownV2')


if __name__ == "__main__":

    updater = Updater(token = os.environ["TOKEN1"], use_context= True)
    dp = updater.dispatcher
    pictopdf = Pic2pdf()
    mergepdf = PdfAppend()

################## Add the handlers to the dispatcher #####################
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(ConversationHandler(

        entry_points= [CommandHandler('photopdf', pictopdf.pictopdfCommandHandlder),
                        CommandHandler('mergepdf', mergepdf.mergePdfCommandHandler)
        ],

        states= {pictopdf.getPicToPdfState(): [MessageHandler(Filters.photo, pictopdf.imputImgs),
                                            MessageHandler(Filters.regex(r"Cancel"),pictopdf.cancel),
                                            MessageHandler(Filters.regex(r"Convert to PDF"),pictopdf.conversionToPDF)],
                
                mergepdf.getPdfAppendStatus():[MessageHandler(Filters.document, mergepdf.pdfInput),
                                            MessageHandler(Filters.regex(r"Cancel"), mergepdf.cancel),
                                            MessageHandler(Filters.regex(r"Merge PDF"), mergepdf.makeMergingProcess),
                                            MessageHandler(Filters.regex(r"One page"), mergepdf.setSelectedMode ),
                                            MessageHandler(Filters.regex(r"[0-9]*"), mergepdf.inputOnePage),
                                            ]
                },

        fallbacks=[]
    ))

updater.start_polling()
updater.idle()