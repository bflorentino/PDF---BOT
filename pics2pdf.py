from BotCommons import BotCommons
import img2pdf
from telegram.ext import ConversationHandler
import os

class Pic2pdf(BotCommons):

    def __init__(self):

        self.__PICTOPDF = 0
        self.images = []
        self.picsSoFar = 0


    def getPicToPdfState(self):

        return self.__PICTOPDF


    def pictopdfCommandHandlder(self, update, context):

        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "Send your pictures", 
                                parse_mode='MarkdownV2')

        return self.__PICTOPDF


################## Gets all the img inputs and saves them in a list #####################
    def imputImgs(self, update, context):
        
        photo = update.message.photo[-1].file_id
        obj = context.bot.get_file(photo)
        self.images.append(obj)
        self.picsSoFar += 1
        text = f"You have sent {self.picsSoFar} pictures so far"

        context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = text, 
                                parse_mode='MarkdownV2')

        super().showKeyboardButtons(update, 
                                context, 
                                [["Convert to PDF", "Cancel"]], 
                                "Press one button or continue sending pictures")


################## Converts the input images into a PDF ##################### 
    def conversionToPDF(self, update, context):
        
        context.bot.send_message(chat_id = update.effective_chat.id, 
                            text = "Starting conversion", 
                            parse_mode = "MarkdownV2")
        
        imagesDownloaded = [image.download() for image in self.images]
            
        try:

            with open("Converted.pdf", "wb") as nf:

                image = img2pdf.convert(imagesDownloaded)
                nf.write(image)
            
            super().sendPdf(update.message.chat, "Converted.pdf",)

        except:

            context.bot.send_message(chat_id = update.effective_chat.id, 
                                text = "There was an error while converting the pictures", 
                                parse_mode = "MarkdownV2")

        finally:

            self.deleteDownloadedImages(imagesDownloaded)
            self.clearData()

            return ConversationHandler.END


    def deleteDownloadedImages(self, images: list):

        for image in dict.fromkeys(images):
            os.unlink(image)


    def clearData(self):

        self.images.clear()
        self.picsSoFar = 0
