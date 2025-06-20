"""Sensor platform for Notification Catcher."""
import logging
import json

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components import mqtt

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_TOPIC = "notification_catcher/notify"
# You might want to make the topic configurable via config flow in the future
# For now, we'll use a default topic.

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    # We are not using config_entry here as topic is hardcoded for now
    # but it's good practice to have it for future config flow.

    sensor = NotificationCatcherSensor(hass, config_entry)
    async_add_entities([sensor])

class NotificationCatcherSensor(SensorEntity):
    """Representation of a Notification Catcher sensor."""

    def __init__(self, hass, config_entry):
        """Initialize the sensor."""
        self.hass = hass
        self._config_entry_id = config_entry.entry_id
        self._name = "Last Notification"  # Or "Notification Catcher"
        self._state = None
        self._attributes = {}
        # Using a unique ID based on the config entry ID for future scalability
        self._attr_unique_id = f"{config_entry.entry_id}_last_notification"

        # Device info: Groups sensors under a single device in HA
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name="Notification Catcher",
            manufacturer="User Custom", # Or your name/GitHub username
            model="MQTT Listener"
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor (e.g., the notification title or timestamp)."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_added_to_hass(self):
        """Subscribe to MQTT events when added to hass."""
        await super().async_added_to_hass()

        @callback
        def message_received(msg):
            """Handle new MQTT messages."""
            _LOGGER.debug(f"Received MQTT message on topic {msg.topic}: {msg.payload}")
            try:
                payload = json.loads(msg.payload)
                title = payload.get("title", "No Title")
                message = payload.get("message", "No Message")

                self._state = title  # Set sensor state to notification title
                self._attributes["title"] = title
                self._attributes["message"] = message
                self._attributes["received_at"] = msg.timestamp if hasattr(msg, 'timestamp') else self.hass.loop.time()
                self._attributes["topic"] = msg.topic

                self.async_write_ha_state()
            except json.JSONDecodeError:
                _LOGGER.error(f"Error decoding JSON: {msg.payload}")
            except Exception as e:
                _LOGGER.error(f"Error processing MQTT message: {e}")

        # Subscribe to the MQTT topic
        # The topic can be made configurable later via ConfigFlow
        await mqtt.async_subscribe(
            self.hass,
            DEFAULT_TOPIC,
            message_received,
            1  # QoS level
        )
        _LOGGER.info(f"NotificationCatcherSensor subscribed to MQTT topic: {DEFAULT_TOPIC}")

    # If you need to unsubscribe, you can do it in async_will_remove_from_hass
    # async def async_will_remove_from_hass(self):
    #     await super().async_will_remove_from_hass()
    #     # Unsubscribe from MQTT topic
    #     # This requires storing the unsubscribe callable returned by async_subscribe
    #     _LOGGER.info("Unsubscribing from MQTT topic...")
