#!/bin/python
# A very simple intent handler, for 'Hello'. This can be used as example.
from IntentHandler import IntentHandler 
# set PYTHONPATH to parent directory for testing !!

import random

class Hello( IntentHandler ):
     def handle(self, name, data):
        replies = ['Hi!', 'Hallo!', 'Hey Du!', 'Tachchen']
        self.speak( random.choice( replies ) )

# a small test
if __name__ == "__main__":

    input = '''{
        "input": "Hallo", 
        "intent": {
            "intentName": "Hello",
            "confidenceScore": 1.0
        }, 
        "siteId": "balin", 
        "id": null, 
        "slots": [], 
        "sessionId": "balin-picovoice-e8399dd3-d534-4f16-9a28-f8a672a994cb", 
        "customData": null, 
        "asrTokens": [[{
            "value": "Hallo", 
            "confidence": 1.0, 
            "rangeStart": 0, 
            "rangeEnd": 5, 
            "time": null
        }]], 
        "asrConfidence": null, 
        "rawInput": "hallo", 
        "wakewordId": "picovoice", 
        "lang": null
        }'''
    o = Hello()
    o.setData( input )
    print( o.getData() )
    o.handle( 'Hello', input )
    print( o.getAnswer() )

