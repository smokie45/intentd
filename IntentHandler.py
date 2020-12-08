# The IntendHandler class defines the basic sceleton of an intent handler.
# Common functions (e.g. like speak()) used by many plugins, can be added here.
import json
import logging
log = logging.getLogger( 'IntentHandler'  )

class IntentHandler:
    intent = None
    answer = None
    siteId = None
    noReaction = False

    # forward some JSON data to intent handler
    def setData( self, data):
        # TODO: verify that handler mataches 'intent' before importing
        self.intent = json.loads( data )
        self.siteId = self.intent['siteId']
        # extract basic values (e.g. siteId, ..)

    # get JSON data from intent handler
    def getData( self ):
        return  self.intent 

    # get a reply from inent handler. This can be called after a handler has been executed.
    # TODO: better to use return value of handle() ?
    def getAnswer( self ):
        if self.noReaction:
            log.info( 'Handler configured to not react!')
            return None
        return self.answer 

    # convert given text to JSON and store in answer
    def speak( self, text):
        a = { "text" : text, "siteId" : self.siteId }
        self.answer = json.dumps( a )

    # function, which is implemented individually by handler and called from external
    # on intent activation.
    # TODO: better to split external trigger call X. X prepares data and calls internal handle(). 
    #       Handle() still implemented by plugin
    def handle( self, name, data ):
        print('No default handling')

