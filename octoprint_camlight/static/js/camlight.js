$(function() {
    function CamlightViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];
        self.settings = null;

        self.speed = ko.observable();
        self.speedValue = ko.pureComputed(function(){
            return self.speed() + "%";
        }, self);

        self.lightsOn = false;
        self.turnoff = function() {
            console.log({off:self.lightsOn});
            if (self.lightsOn == true) {
                self.lightsOn = false;
                self.ledCmd();
            }
        }

        self.turnon = function() {
            console.log({on:self.lightsOn});
            if (self.lightsOn == false) {
                self.lightsOn = true;
                self.ledCmd();
            }
        }

        self.autoOn = ko.observable();

        self.speed.subscribe(function() {
            self.settingsViewModel.saveData({
                "plugins": {
                    "camlight": {
                        "speed": self.speed(),
                        "switch": {
                            "activated": self.lightsOn,
                            "auto_cam": self.autoOn()
                        }
                    }
                }
            });            
        });


        self.ledCmd = function() {
            $.ajax({
                url: API_BASEURL + "plugin/camlight",
                type: "POST",
                dataType: "json",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify({
                    "command": "lights", 
                    "lights_on": self.lightsOn, 
                    "pwm_speed": self.speed()
                })
            });
        }

        self.autoOn = ko.observable(false);

        self.onBeforeBinding = function() {
            self.settings = self.settingsViewModel.settings;
            self.speed(self.settings.plugins.camlight.speed());
            self.lightsOn = self.settings.plugins.camlight.switch.activated();
            self.autoOn(self.settings.plugins.camlight.switch.auto_cam());
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        CamlightViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#sidebar_plugin_camlight"]
    ]);
});
