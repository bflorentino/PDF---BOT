import abc
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram import ChatAction
import os

class BotCommons(abc.ABC):

    def cancel(self, update, context):
        
        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Cancelled", 
                                parse_mode = "MarkdownV2")

        self.clearData()

        return ConversationHandler.END


    def showKeyboardButtons(self, update, context, keyboard, text):

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = text,
                                reply_markup = reply_markup,
                                parse_mode = "MarkdownV2")


    @abc.abstractmethod
    def clearData(self):
        """Clears lists"""


####### Send output PDF to chat ######
    def sendPdf(self,  chat, filename):

        chat.send_action(
            action = ChatAction.UPLOAD_DOCUMENT, timeout = None
        )
        chat.send_document(
            open(filename, "rb")
        )

        os.unlink(filename)