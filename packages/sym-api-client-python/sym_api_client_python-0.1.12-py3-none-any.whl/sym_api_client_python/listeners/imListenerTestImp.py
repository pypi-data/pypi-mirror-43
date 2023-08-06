from .imListener import IMListener
import logging
#sample implementation of Abstract imListener class
#has instance of SymBotClient so that it can respond to events coming in by leveraging other clients on SymBotClient
#each function should contain logic for each corresponding event
class IMListenerTestImp(IMListener):

    def __init__(self, SymBotClient):
        self.botClient = SymBotClient

    def onIMMessage(self, IMmessage):
        logging.debug('message recieved in IM', IMmessage)

    def onIMCreated(self, IMCreated):
        logging.debug('IM created!', IMCreated )
