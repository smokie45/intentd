#!/bin/python
from IntentHandler import IntentHandler 
# set PYTHONPATH to parent directory for testing !!
import random

class Test( IntentHandler ):
     def handle(self, name, data):
        self.speak( 'Frohe Weihnachten' )


# a small test
if __name__ == "__main__":
    None
