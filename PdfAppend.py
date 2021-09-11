from BotCommons import BotCommons
import PyPDF2
from telegram.ext import ConversationHandler
import os

class PdfAppend(BotCommons):


    def __init__(self):

        self.__PDFAPPEND = 1
        self.documents = []
        self.merger = PyPDF2.PdfFileMerger()
        self.pdfSoFar = 0
        self.currentDoc = None
        self.merged = False


    def getPdfAppendStatus(self):

        return self.__PDFAPPEND



    def mergePdfCommandHandler(self, update, context):

        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Send the pdf files in the order you want them to be merged",
            parse_mode = "MarkdownV2"
        )

        return self.__PDFAPPEND
    

########## Gets all the pdf by the user sent and saves them in a list #################
    def pdfInput(self, update, context):

        document = update.message.document

        try:

            assert(document.file_name.endswith("pdf"))
            obj = context.bot.get_file(document)
            self.documents.append(obj)

            super().showKeyboardButtons(
                                    update, 
                                    context, 
                                    [["Merge PDF", "Cancel"]],
                                    "Press one buttom below or continue sending PDF Documents" )
            
            self.pdfSoFar += 1
            text = f"You have sent {self.pdfSoFar} pdf documents so far"

            context.bot.send_message(chat_id = update.effective_chat.id, 
                                    text = text,
                                    parse_mode = "MarkdownV2")

        except AssertionError:

            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "No Pdf detected. The merging process will be cancelled",
                parse_mode = "MarkdownV2"
            )

            return ConversationHandler.END


############## Re-initialze the object attributes ############
    def clearData(self):

        self.documents.clear()
        self.pdfSoFar = 0
        self.currentDoc = None
        self.merged = False


##### When the user is done with sending, pdf files will be merged in an only new PDF pdf through this method ########
    def makeMergingProcess(self, update, context):

        context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "Merging files, please wait",
                parse_mode = "MarkdownV2"
        )

        for document in range(len(self.documents)):

            self.currentDoc = self.documents[document].download()
            
            if self.mergePDF(self.currentDoc) == False:

                break
        
        if self.merged:

            newPdf = self.makeNewPdf()
            super().sendPdf(update.message.chat, newPdf)
        
        else:

            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "An error occured while merging pdfs, so merging process was cancelled",
                parse_mode = "MarkdownV2"
            )

            self.clearData()

        return ConversationHandler.END


####### It merges every file received ######
    def mergePDF(self, filename):

        try:

            with open(filename, "rb") as file:

                reader = PyPDF2.PdfFileReader(file)
                self.merger.append(reader)

            self.merged = True

        except:

            self.merged = False

        finally:

            os.unlink(filename)
            return self.merged


####### When the merging is done the output pdf will be gotten through this method
    def makeNewPdf(self):

        self.merger.write("merged.pdf")
        return "merged.pdf"