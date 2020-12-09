# intend - A small intent handling daemon

Intend can react to intent triggers from [HERMES](https://snips.gitbook.io/tutorials/t/technical-guides/listening-to-intents-over-mqtt-using-python) MQTT. Plugins are in charge to handle the intents.

### TODO:
* use dynamic user for systemd service
* move handlers to /var/lib/intentd
* link 'intentd' to /usr/bin
* add option (--list) to show installed handlers
* use inotify to get aware on new handlers
* make intentd a singleton to allow subsequent call to configure without starting new instance
** include option to force having 2nd instance
* handlers
** Teatimer
** Tagesrückblick
** Meine Termine

