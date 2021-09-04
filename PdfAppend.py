from BotCommons import BotCommons
import PyPDF2
from telegram import ChatAction
from telegram.ext import ConversationHandler, conversationhandler
import os
from telegram import ReplyKeyboardMarkup
import multiprocessing


class PdfAppend(BotCommons):

    __PDFAPPEND = 1
    documents = []
    merger = PyPDF2.PdfFileMerger(True)
    pdfSoFar = 0
    currentPages = 0
    onePage = 0
    currentDoc = None
    mergingMode = None
    rangePage = []


    def __init__(self) -> None:
        pass 


    def getPdfAppendStatus(self):

        return self.__PDFAPPEND


    def mergePdfCommandHandler(self, update, context):

        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Send the pdf files in the order you want them to be merged",
            parse_mode = "MarkdownV2"
        )

        return self.__PDFAPPEND
    

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


    def clearData(self):

        self.documents.clear()
        self.pdfSoFar = 0
        self.currentPages = 0
        self.onePage = 0
        self.currentDoc = None
        self.mergingMode = None
        self.rangePage = []


    def makeMergingProcess(self, update, context):

        for document in range(len(self.documents)):

            self.currentDoc = self.documents[document].download()
            doc = PyPDF2.PdfFileReader(open(self.currentDoc, "rb"))
            self.currentPages = doc.getNumPages()
            
            super().showKeyboardButtons(update, 
                                        context, 
                                        [["One Page", "Pages range", "Full document", "Cancel"]],
                                        f"Select the mode in which pdf {document + 1} will be merged")
                

        newPdf = self.makeNewPdf()
        self.sendPdf(newPdf, update.message.chat)
        self.clearData()

        return ConversationHandler.END


    def askOnePage(self, update, context):
        
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"Start page to append from this file? This file has {self.currentPages} pages",
            parse_mode = "MarkdownV2"
        )


    def inputOnePage(self, update, context):

        if self.mergingMode == 0:

            self.onepage = int(update.message.text)
            self.mergePDF(self.currentDoc)
        
        elif self.mergingMode == 1:
            
            self.rangePage.append(int(update.message.text))

            if len(self.rangePage) == 2:
                self.mergePDF(self.currentDoc)

        else:
            self.mergePDF(self.currentDoc)




    def setSelectedMode(self, update, context):

        text = update.message.text

        if text == "One page":

            self.mergingMode = 0
            self.askOnePage(update, context)

        elif text == "Range page":

            self.mergingMode = 1
            
            for i in range(2):
                self.askOnePage(update, context)

        else:
            self.mergingMode = 2


    def mergePDF(self, filename):


        if self.mergingMode == 0:
            self.merger.append(filename, self.onePage)
        
        elif self.mergingMode == 1:
            self.merger.append(filename, range(self.rangePage[0], self.rangePage[1] + 1 ))
        
        else:
            self.merger.append(filename)

        os.unlink(filename)


    lambda self: self.merger.write("merged.pdf") 


    def sendPdf(self, chat, filename):

        chat.send_action(
            action =   ChatAction.UPLOAD_filenameUMENT
        )

        chat.send_document(
            document = open(filename,  "rb")
        )


