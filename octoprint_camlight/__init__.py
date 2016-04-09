# coding=utf-8
from __future__ import absolute_import
import os, os.path
import octoprint.plugin
import socket
from subprocess import Popen

sockpath = "/var/run/gpio.sock"
daemon = 0
client = 0

class CamlightPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.ShutdownPlugin,
                     octoprint.plugin.TemplatePlugin,
                     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.SimpleApiPlugin):

    def on_after_startup(self):
        global __plugin_name__
        global client
        global sockpath
        global daemon
        daemon = Popen(["sudo", "python", "gpiopwm.py"])
        if os.path.exists(sockpath):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            client.connect(sockpath)
        self._logger.info(__plugin_name__ + " started!")

    def on_shutdown():
        global client
        if client <> 0:
            client.close()
        
    def get_settings_defaults(self):
        return dict(
            speed = 50,
            switch = dict(
                activated = False,
                auto_cam = True
            )
        )

    def get_template_configs(self):
        return [
            dict(type="sidebar", custom_bindings = False)
        ]

    def get_assets(self):
        return dict(
            js=["js/camlight.js"]
        )

    def get_api_commands(self):
        return dict(
            lights=[]
        )

    def on_api_command(self, command, data):
        import flask
        global client
        if command == "lights":
            speed = self._settings.get(["speed"])
            lights_on = self._settings.get(["switch", "activated"])
            if "lights_on" in data:
                lights_on = data["lights_on"]
            if "pwm_speed" in data:
                speed = data["pwm_speed"]
                
            if lights_on == False:
                x = raw_input("stp")
            else:
                x = raw_input("set "+ str(speed))
            if not client:
                self._logger.error("Client Socket not started!")
            else:
                client.send(x)

    def on_api_get(self, request):
        return flask.jsonify(camlight_active=true)

        

__plugin_name__ = "OctoPrint-Camlight"
__plugin_implementation__ = CamlightPlugin()

