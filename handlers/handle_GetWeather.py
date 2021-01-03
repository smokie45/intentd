#!/bin/python
# An intent handler to handle weather requests. It'll download a weather forecast from
# german DWD, do some parsing and return the text as speech.
from IntentHandler import IntentHandler 
# set PYTHONPATH to parent directory for testing !!
import logging
log = logging.getLogger( 'GetNews' )

import re
import urllib.request

class GetWeather( IntentHandler ):
    noReaction = False              # flag to disable answering
    def handle( self ):
        time = self.slots['wetter']
        url = 'https://www.dwd.de/DWD/wetter/wv_allg/deutschland/text/vhdl13_dwhg.html'
        req = urllib.request.Request( url )
        response = urllib.request.urlopen(req)
        response.encoding = 'utf8'
        a = response.read().decode('latin-1')
        # cut out the wanted weather section
        start = 'Detaillierter Wetterablauf:'
        stop =  '</pre>'
        wanted = False
        out = {} 
        days = 4 
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        for l in a.splitlines():
            # print(l)
            if stop in l:
                if wanted:
                    # remove HTML tags
                    n = re.sub(cleanr, '', n)
                    # remove line feeds
                    n = n.replace('\n', ' ').replace('\r', '')
                    out[ day ] =  n
                    n = ''
                    day += 1
                    # print("day = " + str(day))
                    if day >= days:
                        wanted = False
            if wanted:
                n += l
            if start in l:
                day = 0
                n=''
                wanted = True
        # print( out )
        if time == 'morgen':
            txt = out[1]
        elif time == 'übermorgen':
            txt = out[2]
        else:
            txt = out[0]
        return txt 


if __name__ == "__main__":

    input = '''{
        "input": "Wie wird das Wetter morgen", 
        "intent": {
            "intentName": "GetWeather", 
            "confidenceScore": 1.0 
        }, 
        "siteId": "balin", 
        "id": null, 
        "slots": [{
            "entity": "wetter", 
            "value": {
                "kind": "Unknown", 
                "value": "morgen" 
            }, 
            "slotName": "wetter", 
            "rawValue": "morgen", 
            "confidence": 1.0, 
            "range": {
                "start": 20, 
                "end": 26, 
                "rawStart": 20, 
                "rawEnd": 26
            }
        }], 
        "sessionId": "balin-picovoice-bdb7c42a-2d61-45fb-a695-819e8669e66d", 
        "customData": null, 
        "asrTokens": [[{
            "value": "Wie", 
            "confidence": 1.0, 
            "rangeStart": 0, 
            "rangeEnd": 3, 
            "time": null
        }, { 
            "value": "wird", 
            "confidence": 1.0, 
            "rangeStart": 4, 
            "rangeEnd": 8, 
            "time": null
        }, {
            "value": "das", 
            "confidence": 1.0, 
            "rangeStart": 9, 
            "rangeEnd": 12, 
            "time": null
        }, {
            "value": "Wetter", 
            "confidence": 1.0, 
            "rangeStart": 13, 
            "rangeEnd": 19, 
            "time": null
        }, {
            "value": "morgen", 
            "confidence": 1.0, 
            "rangeStart": 20, 
            "rangeEnd": 26, 
            "time": null 
        }]], 
        "asrConfidence": null, 
        "rawInput": "wie wird das wetter morgen", 
        "wakewordId": "picovoice", 
        "lang": null
    }'''
    log.setLevel( logging.DEBUG)
    o = GetWeather()
    o.doHandle( input )
    print( o.answer )
