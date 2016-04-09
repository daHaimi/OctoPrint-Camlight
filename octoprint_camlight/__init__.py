# coding=utf-8
from __future__ import absolute_import
from subprocess import call
import octoprint.plugin

class CamlightPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.ShutdownPlugin,
                     octoprint.plugin.TemplatePlugin,
                     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.SimpleApiPlugin):

    def on_after_startup(self):
        global __plugin_name__
        self._logger.info(__plugin_name__ + " started!")

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings = False),
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
        if command == "lights":
            speed = self._settings.get(["speed"])
            lights_on = self._settings.get(["switch", "activated"])
            if "lights_on" in data:
                lights_on = data["lights_on"]
            if "pwm_speed" in data:
                speed = data["pwm_speed"]
            call(["sudo", "python", "gpiopwm.py", "--speed", str(speed), "--lon", str(lights_on).lower()])
            self._logger.info(command + " called with " + str(lights_on).lower() + " " + str(speed))

    def on_api_get(self, request):
        return flask.jsonify(camlight_active=true)

        

__plugin_name__ = "OctoPrint-Camlight"
__plugin_implementation__ = CamlightPlugin()

