import logging

import voluptuous as vol

from homeassistant.const import CONF_HOST
from homeassistant.components.light import ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['webthing_hass==1.0.0']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Webthing Light platform."""
    import webthing_hass

    host = config.get(CONF_HOST)
    hub = wething_hass.Hub(host)

    if not hub.is_connected():
        _LOGGER.error("Could not connect to webthing host")
        return

    add_devices(WebthingLight(light) for light in hub.lights())


class WebthingLight(Light):
    """Representation of an Webthing Light."""

    def __init__(self, light):
        """Initialize an WebthingLight."""
        self._light = light
        self._name = light.name
        self._state = None
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._light.brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._light.turn_on()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.turn_off()

    def update(self):
        """Fetch new state data for this light."""
        self._light.update()
        self._state = self._light.is_on()
        self._brightness = self._light.brightness
