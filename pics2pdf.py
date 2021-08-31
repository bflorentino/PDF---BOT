import img2pdf
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import os
from PIL import Image
from telegram import ChatAction


class Pic2pdf():

    __PICTOPDF = 0
    images = []
    picsSoFar = 0

    def __init__(self) -> None:
        pass


    def getPicToPdfState(self):

        return self.__PICTOPDF


    def pictopdfCommandHandlder(self, update, context):

        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Send your pictures", 
                                parse_mode='MarkdownV2')

        return self.__PICTOPDF


    def imputImgs(self, update, context):
        
        photo = update.message.photo[-1].file_id
        obj = context.bot.get_file(photo)
        self.images.append(obj)
        self.picsSoFar += 1
        text = f"You have sent {self.picsSoFar} pictures so far"

        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = text, 
                                parse_mode='MarkdownV2')

        self.showKeyboardButtons(update, context)


    def showKeyboardButtons(self, update, context):
        
        keyboard = [["Convert to PDF", "Cancel"]]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Press one buttom below or continue sending pictures",
                                reply_markup = reply_markup,
                                parse_mode = "MarkdownV2")


    def cancel(self, update, context):
        
        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Cancelled", 
                                parse_mode = "MarkdownV2")

        self.clearData()

        return ConversationHandler.END 


    def conversionToPDF(self, update, context):
        
        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Starting conversion", 
                                parse_mode = "MarkdownV2")

        imagesDownloaded = [image.download() for image in self.images]
        
        try:

            with open("Converted.pdf", "wb") as nf:

                image = img2pdf.convert(imagesDownloaded)
                nf.write(image)

        except:

            context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "There was an error while converting the pictures", 
                                parse_mode = "MarkdownV2")

            self.sendPDF("Converted.pdf", update.message.chat)

        finally:

            self.deleteDownloadedImages(imagesDownloaded)
            self.clearData()

            return ConversationHandler.END


    def deleteDownloadedImages(self, images: list):

        for image in images:
            os.unlink(image)


    def sendPDF(self, filename, chat):

        chat.send_action(
            action = ChatAction.UPLOAD_DOCUMENT
        )
        chat.send_document(
            open(filename, "rb")
        )

        os.unlink(filename)


    def clearData(self):

        self.images.clear()
        self.picsSoFar = 0