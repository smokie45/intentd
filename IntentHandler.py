# The IntendHandler class defines the basic sceleton of an intent handler.
# Common functions (e.g. like speak()) used by many plugins, can be added here.
import json
import logging
log = logging.getLogger( 'IntentHandler'  )

class IntentHandler:
    intent = None       # full intent data
    slots  = None       # dict of slots
    answer = None       # reply given by handler
    siteId = None       # the rhasspy siteID 
    noReaction = False

    # triggered when intent was activated. Data will be provided. On return, an answer is provided 
    def doHandle( self, data):
        # TODO: verify that handler mataches 'intent' before importing
        self.intent = json.loads( data )
        self.siteId = self.intent['siteId']
        # log.debug(">-- SLOT EXTRACTION ---")
        # extract slots from intents to make them easy accessible
        for s in self.intent['slots']:
            log.debug("  SLOT="+ s['entity'] + ", value=" + s['value']['value'] )
            self.slots[ s['entity'] ] = s['value']['value']
        # log.debug("<-- SLOT EXTRACTION ---")
        self.answer = self.handle()
        if self.answer:
            # answer is not 'None', add siteID
            self.answer = json.dumps( { 'text' : self.answer, 'siteId' : self.siteId } )

        return self.answer

    # get JSON data from intent handler
    # def getData( self ):
    #     return  self.intent 
    #
    # # get a reply from inent handler. This can be called after a handler has bVeen executed.
    # # TODO: better to use return value of handle() ?
    # def getAnswer( self ):
    #     if self.noReaction:
    #         log.info( 'Handler configured to not react!')
    #         return None
    #     return self.answer 
    #
    # # convert given text to JSON and store in answer
    # def speak( self, text):
    #     a = { "text" : text, "siteId" : self.siteId }
    #     self.answer = json.dumps( a )

    # function, which is implemented individually by handler 
    def handle( self ):
        print('No default handling')

