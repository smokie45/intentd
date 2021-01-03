#!/bin/python
# This intent handler will fetch a given number of new via RSS from tageschau.de
# A hash of each played news is stored, to avoid a news is played twice.
from IntentHandler import IntentHandler 
# set PYTHONPATH to parent directory for testing !!
import logging
log = logging.getLogger( 'GetNews' )

import feedparser
import hashlib

class GetNews( IntentHandler ):
    noReaction = False              # flag to disable answering
    url = 'https://www.tagesschau.de/xml/atom/'
    done = [] # list of hashes from entries already played

    def handle( self ):
        # get number of news slot
        n = int(self.slots['News'])
        log.info('Num of news to speak:=' + str(n))
        reply=''
        # get number of news and concate them
        for x in range( n ):
            # get 'n' news and concate them as one string
            reply += self.getNewItem( self.url ) + ".\n\n"
        return reply

    def getNewItem( self, url ):
        d = feedparser.parse( url )
        allHash = []    # temporary list of hashes for al feed entries
        # create list of hashes for all items in feed
        for item in d.entries:
            h = hashlib.md5( item.description.encode() ).hexdigest()
            allHash.append( h )
        # remove items available in done list, but not in allHash list
        for h in self.done:
            if h not in allHash:
                # print('Removing: '+h)
                self.done.remove( h )

        # find first item, where hash is not in done list
        for item in d.entries:
            h = hashlib.md5( item.description.encode() ).hexdigest()
            log.debug('News hash is:' + h + ' - done is:'+ str(self.done) )
            if h not in self.done:
                self.done.append( h )    # add new hash to done list
                # print( item.title + '[' + item.updated+ ']' )
                # print( ' -> ' + item.description)
                return item.title + '! ' + item.description
            # print( ' SKIP '),
        # end of items. Maybe all are played ?
        return 'Es gibt keine neuen Schlagzeilen!'


if __name__ == "__main__":
    print( getNewItem( url ) )
    print( getNewItem( url ) )
    print( getNewItem( url ) )

