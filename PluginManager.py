#!/bin/python
#
# The PluginManager class implenets en extension mechanismus for python. At instanciation
# the given 'plugindir' folder is parsed for available plugins. 
# Plugins are python modules. The plugin name is  prefixed with self.pluginprefix.
# Each module has a class definiton which is named according to the plugin.
# Example:
#           plutings/plugin_a.py:
#               class a: ....
import importlib.util
import sys
import os


# self.plugindir dwill contain a list of plugins
class PluginManager:
    plugins = []        # list of plugin names
    instances = {}      # dict of plugin names and a reference to their instance
    plugindir = ''      # name of the plugin folder to scan
    pluginprefix = ''   # prefix for plugin name

    def __init__(self, plugindir, pluginprefix):
        self.plugindir = plugindir
        self.pluginprefix = pluginprefix

        self.findPlugins()      # find all plugins
        self.getInstances()     # and instanciate them

    # Get list of plugins, contained in self.plugindir and having self.pluginprefix
    def findPlugins(self):
        files = os.listdir( self.plugindir )
        for f in files:
            if f.startswith( self.pluginprefix ):
                f = f.removeprefix( self.pluginprefix )
                f = f.removesuffix( '.py' )
                self.plugins.append( f)

    # Instanciate all known plugins 
    def getInstances( self ):
        for plugin in self.plugins:
            try:
                # import the module
                _a = importlib.import_module( '.' + self.pluginprefix + plugin, package = self.plugindir )
                cls = getattr( _a, plugin)              # get class
                self.instances[ plugin ] = cls()        # create instance and store ref in dict
            except ImportError as err:
                print('Error:', err)

    # return a list of all plugin names
    def getPlugins( self ):
        return self.plugins

    # return an instance of the plugin for the given  name
    def getPlugin( self, name):
        if name in self.instances:
            return self.instances[ name ]
        else:
            print('Intent \'' + name + '\' not found!')


# a small unit test
if __name__ == "__main__":
    mgr = PluginManager( 'handlers', 'handle_' )
    intent = 'Hello'
    o = mgr.getPlugin( intent )
    if o:
        o.handle()
