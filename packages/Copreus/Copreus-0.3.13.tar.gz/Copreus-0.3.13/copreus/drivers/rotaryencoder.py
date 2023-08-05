from time import time
import RPi.GPIO as GPIO
from copreus.baseclasses.adriver import ADriver
from copreus.baseclasses.aevents import AEvents
from copreus.schema.rotaryencoder import get_schema


class RotaryEncoder(ADriver, AEvents):
    """Driver for rotary encoder like the KY-040 with software solutions for debouncing and direction detection.

    The driver entry in the yaml file consists of:
      * ADriver entries
        * topics_pub:
          * rotate - mqtt-translations.rotate-left and mqtt-translations.rotate-right
          * button_pressed - mqtt-translations.button_pressed
          * button_state - mqtt-translations.button_state-open and mqtt-translations.button_state-closed
      * RotaryEncoder entries
        * sw: gpio pin for pressing the rotary encoder
        * dt: dt gpio pin
        * clk: clk gpio pin

    Example:
    device:
        type: rotaryencoder
        pin_sw:  12
        pin_dt:  16
        pin_clk: 20
        topics-pub:
            rotate: /input1/rotate
            button_pressed: /input1/button/pressed
            button_state:   /input1/button/state
        mqtt-translations:
            rotate-left: LEFT
            rotate-right: RIGHT
            button_pressed: PRESSED
            button_state-open: OPEN
            button_state-closed: CLOSED

    """

    _clk = -1  # clk gpio pin id
    _dt = -1  # dt gpio pin id
    _sw = -1  # sw gpio pin id
    _last_clk = -1  # last clk value - used for rotation direction detection
    _last_time = -1 # time stamp of the last rotation step
    _last_direction = 0  # rotation direction of the last rotation step
    _min_time_gap = 0.100  # minimum time gap between direction changes
    _LEFT = -1  # internal constant - rotation direction left
    _RIGHT = 1  # internal constant - rotation direction right

    def __init__(self, config, mqtt_client=None, logger=None, stdout_log_level=None, no_gui=None,
                 manage_monitoring_agent=True):
        ADriver.__init__(self, config, mqtt_client, logger, logger_name=__name__,
                         stdout_log_level=stdout_log_level, no_gui=no_gui,
                         manage_monitoring_agent=manage_monitoring_agent)
        AEvents.__init__(self, self._config, self._logger)

        self._clk = self._config["pin_clk"]
        self._dt = self._config["pin_dt"]
        self._sw = self._config["pin_sw"]

        self._add_event(self._clk, self._callback_rotary, 1)
        self._add_event(self._sw, self._callback_sw)

        self._last_time = time()

    def _callback_sw(self, channel):
        """Event handler for gpio pin 'sw'. Publishes to the topics 'button_state' and 'button_pressed'."""
        self._logger.info("SW-event detected.")
        state = GPIO.input(self._sw)
        if not state:
            self._publish_value(self._topics_pub["button_pressed"], self._mqtt_translations["button_pressed"])
            self._publish_value(self._topics_pub["button_state"], self._mqtt_translations["button_state-closed"])
        else:
            self._publish_value(self._topics_pub["button_state"], self._mqtt_translations["button_state-open"])

    def _callback_rotary(self, channel):
        """Event handler for gpio pin 'clk'. Detects the rotation direction and filters out 'rotation bounces' -
        rotation direction changes that happen to fast und are thus considered to originiate in bounces. Publishes
        to the topic 'rotate'."""
        akt_clk = GPIO.input(self._clk)
        akt_time = time()
        self._logger.info("Rotary-event detected.")

        if akt_clk != self._last_clk:
            rotate = self._LEFT
            if GPIO.input(self._dt) != akt_clk:
                rotate = self._RIGHT

            #filter
            if akt_time - self._last_time < self._min_time_gap and rotate != self._last_direction:
                self._logger.info("Time between direction change to small - skipping this event.")
            else:
                if rotate == self._RIGHT:
                    self._publish_value(self._topics_pub["rotate"], self._mqtt_translations["rotate-right"])
                else:
                    self._publish_value(self._topics_pub["rotate"], self._mqtt_translations["rotate-left"])
                self._last_direction = rotate
                self._last_time = akt_time
        self._last_clk = akt_clk

    def _driver_start(self):
        """ADriver._driver_start"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._last_clk = GPIO.input(self._clk)
        self._register_events()

    def _driver_stop(self):
        """ADriver._driver_stop"""
        self._unregister_events()
        GPIO.cleanup(self._dt)
        GPIO.cleanup(self._sw)
        GPIO.cleanup(self._clk)

    @classmethod
    def _get_schema(cls):
        return get_schema()

    def _runtime_information(self):
        return {}

    def _config_information(self):
        return {}


def standalone():
    """Calls the static method RotaryEncoder.standalone()."""
    RotaryEncoder.standalone()


if __name__ == "__main__":
    RotaryEncoder.standalone()
