import abc
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

class BotCommons(abc.ABC):

    def cancel(self, update, context):
        
        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Cancelled", 
                                parse_mode = "MarkdownV2") 

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