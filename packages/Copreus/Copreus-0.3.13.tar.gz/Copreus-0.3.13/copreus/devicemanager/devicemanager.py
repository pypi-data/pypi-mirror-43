from threading import Lock
from pelops.abstractmicroservice import AbstractMicroservice
from copreus.devicemanager.devicefactory import DeviceFactory
from copreus.schema.devicemanager import get_schema
from copreus import version


class DeviceManager(AbstractMicroservice):
    """Takes a yaml config file, creates all devices that are set to active, and starts them.

    The DeviceManager alters the behavior of the devices at three points:
      * A single instance of MyMQTTClient is provided to all driver.
      * It overrides the individual topic_sub_handler and provides one central _on_message handler.
      * One spi lock is provided to avoid overallocation of the spi interface (Please be note that a single lock is
      used for all spi instances independet of the bus/devices parameter. Thus, even in case of two independent spi
      interfaces only one of them can be used at any given time.)

    See copreus.baseclasses.adriver for a brief description of the yaml config file."""

    _version = version

    _devices = None  # list of instantiated devices.
    _spi_lock = None  # threading.Lock for spi interface access
    _i2c_lock = None  # threading.Lock for i2c interface access

    def __init__(self, config, mqtt_client=None, logger=None, stdout_log_level=None, no_gui=None):
        AbstractMicroservice.__init__(self, config, "devices", mqtt_client, logger,
                                      stdout_log_level=stdout_log_level, no_gui=no_gui)
        self._spi_lock = Lock()
        self._i2c_lock = Lock()
        # create_devices needs the full config structure - thus, config instead of self._config is used.
        self._devices = DeviceFactory.create_devices(config, self._mqtt_client, self._logger,
                                                     self._spi_lock, self._i2c_lock)

    def _start(self):
        """Starts all active devices."""
        print("DeviceManager started")
        for device in self._devices:
            device.start()

    def _stop(self):
        """Stops all active devices."""
        for device in self._devices:
            device.stop()
        print("DeviceManager stopped")

    @classmethod
    def _get_description(cls):
        return "Device Manager\n" \
               "In Greek mythology, Copreus (Κοπρεύς) was King Eurystheus' herald. He announced Heracles' Twelve " \
               "Labors. This script starts severaö device driver on a raspberry pi and connects them to MQTT. " \
               "Thus, copreus takes commands from the king (MQTT) and tells the hero (Device) what its labors " \
               "are. Further, copreus reports to the king whatever the hero has to tell him."

    @classmethod
    def _get_schema(cls):
        return get_schema()

    def runtime_information(self):
        info = {
            "devices": []
        }
        for device in self._devices:
            info["devices"].append(device.runtime_information())
        return info

    def config_information(self):
        info = {
            "devices": []
        }
        for device in self._devices:
            info["devices"].append(device.config_information())
        return info


def standalone():
    """Calls the static method DeviceManager.standalone()."""
    DeviceManager.standalone()


if __name__ == "__main__":
    DeviceManager.standalone()
