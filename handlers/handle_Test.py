#!/bin/python
from IntentHandler import IntentHandler 
# set PYTHONPATH to parent directory for testing !!
import random

class Test( IntentHandler ):
     def handle( self ):
        replies = ['Frohe Weihnachten!', 'Herzlichen Glückwunsch', 'Frohe Ostern', 'Frohes neues Jahr', 'Hellau']
        return random.choice( replies )

# a small test
if __name__ == "__main__":
    None
