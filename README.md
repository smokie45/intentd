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
<<<<<<< HEAD
* add threadding or async loops for handlers
* add some diagrams :https://github.com/shd101wyy/markdown-preview-enhanced/blob/master/docs/diagrams.md
=======
* handlers
  * Teatimer
  * Tagesrückblick
  * Meine Termine
>>>>>>> 33f2d5f0a743bc01bbf26376aa59d1e07c3d9184

