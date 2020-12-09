# A simple intent handler to handler time requests in german language
from IntentHandler import IntentHandler 
import datetime

class GetTime( IntentHandler ):
    noReaction = False
    def handle(self ):
        now = datetime.datetime.now()
        return ( "Es ist " + self.t2str(now.hour, now.minute ))


    # convert hour and minute into a string 
    def t2str( self, hour, min):
        if hour > 12:
             hour -= 12
        if  min == 0:
            s = str(hour) + " Uhr"
        elif min == 15:
            s = "viertel nach " + str(hour)
        elif min == 45:
            s = "viertel vor " + str((hour % 12)+1)
        elif min == 30: 
            s = "halb " + str(hour)
        elif min <= 30:
            s = str(min) + " minuten nach " + str(hour)
        elif min > 30:  
            s = str(60-min) + " minuten vor " + str((hour % 12) +1 )
        return s


