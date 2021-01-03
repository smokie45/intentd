#!/bin/python
#
# intend is a small daemon which can react to HERMES intents, provided on MQTT.
# Intent handlers are plugins, which are recognized at startup. Intend will 
# automatically subscribe# to the Hermes intend and trigger the plugin on activation.
# Plugins are python scripts, located in the 'handlers/' subdirectory. The naming schema 
# is 'handler_INTENT.py', where INTENT is the name of the intent the plugin will handle.
#
# Dependencies:
#   python-paho
#
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import logging
import logging.handlers
import sys
import time
import argparse
import json
import PluginManager

# callback for all subscribed topics
def on_mqtt( client, userdata, msg ):
    log.debug("on_mqtt: '"+msg.topic+"' -> '" + str(msg.payload) +"'")
    if msg.topic.startswith('hermes/intent/'):
        intent = msg.topic.split('/')[2]
        # get plugin instance for intant
        o = userdata.getPlugin( intent )
        if o:
            answer = o.doHandle( msg.payload)
            if answer:
                client.publish('hermes/tts/say', answer )
        else:
            log.debug('No registered handler for \'' + intent + '\'')
# callback on connection to mqtt server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("connected to mqtt server")
        client.isConnected = True
    else:
        log.error("on_connect: failed to connect to mqtt server")

# callback on subsription to an mqtt topic
# def on_subscribe( client, userdata, mid, granted_qos):
#     log.debug("on_subscribe:")

# callback for paho-mqtt internal logging
def on_log( client, userdata, level, buf):
    if "PING" not in buf:
        log.debug("on_log: " + buf)


# get name of program. Remove prefixed path and postfixed fileytpe
myName = sys.argv[0]
myName = myName[ myName.rfind('/')+1: ]
myName = myName[ : myName.find('.')]

my_parser = argparse.ArgumentParser(description='intend: Handling intents received via Hermes MQTT')
my_parser.add_argument('--handlers',
    required=False,
    type=str,
    default="handlers",
    help='Set directory for handlers (Default: handlers]')

my_parser.add_argument('--server',
    required=False,
    type=str,
    default="legolas:1883",
    help='Address of MQTT server [NAME:PORT]')
my_parser.add_argument('--verbose',
                       required=False,
                       type=str,
                       default="ERROR",
                       metavar='LEVEL',
#                       choices= ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Set loglevel to [DEBUG, INFO, ..]')
my_parser.add_argument('--log2file',
                       required=False,
                       action='store_true',
                       help='If given, logs are copied to file \'/tmp/' + myName + '.log\'')
args = my_parser.parse_args()
print("Started " + myName )

# setup loggers
logging.basicConfig(
    format='%(levelname)7s: %(message)s',
    level = getattr(logging, args.verbose.upper())
)
log = logging.getLogger( __name__ )
#log.addHandler( logging.StreamHandler(sys.stdout) )
if args.log2file:
    print('Logging to: /tmp/'+myName+'/.log')
    #TODO: add timestamps
    log.addHandler( logging.handlers.RotatingFileHandler('/tmp/'+myName+'.log', maxBytes=2000,  backupCount=1))

# find and instanciate plugins
mgr = PluginManager.PluginManager( args.handlers, 'handle_' )

# create mqtt client
mqttC              = mqtt.Client( client_id = myName, userdata=mgr )
mqttC.isConnected  = False      # connection flag
mqttC.on_connect   = on_connect
mqttC.on_message   = on_mqtt
# mqttC.on_subscribe = on_subscribe
mqttC.on_log       = on_log
mqttC.loop_start()              # create rx/tx thread in background

server = args.server.split(':')[0]
port   = args.server.split(':')[1]
try:
    log.debug('Connecting to \'' + server + ':' + port + '\'') 
    mqttC.connect( server, int(port), 10)
except:
    log.error("Failed to connect to mqtt server. Retry in 2 secs ....")
while not mqttC.isConnected:
        time.sleep(1)           # wait till mqtt server arrives.

# subscribe for all Hermes MQTT intents we have handlers for
for intent in mgr.getPlugins():
    topic = 'hermes/intent/' + intent
    mqttC.subscribe( topic, 0 )

print('Connected to '+server+':'+port+' waiting to handle intents.')
print('Press CTRL-C to stop')
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    state='stop'
    time.sleep(1)
    mqttC.loop_stop()
    mqttC.disconnect()
print('Terminated')

