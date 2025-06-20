"""Config flow for Notification Catcher integration."""
import logging

from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN  # Make sure .const has DOMAIN

_LOGGER = logging.getLogger(__name__)

class NotificationCatcherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Notification Catcher."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            # Config entry already exists, only one instance allowed
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # No data to store from the user in this simple case
            _LOGGER.info("Setting up Notification Catcher integration")
            return self.async_create_entry(title="Notification Catcher", data={})

        # Show a form to the user to confirm setup.
        # Since there's no input, it's just a confirmation.
        return self.async_show_form(
            step_id="user",
            data_schema=None, # No fields needed
            description_placeholders={
                "docs_url": "https://github.com/your_username/ha-notification-catcher#readme"
                # Replace with actual docs url or remove if not needed for form
            },
            errors={}, # No errors to show initially
        )

    # Example of how to implement options flow if you add configurable settings later
    # @staticmethod
    # @callback
    # def async_get_options_flow(config_entry):
    #    return NotificationCatcherOptionsFlowHandler(config_entry)

# class NotificationCatcherOptionsFlowHandler(config_entries.OptionsFlow):
#    def __init__(self, config_entry: config_entries.ConfigEntry):
#        self.config_entry = config_entry
#
#    async def async_step_init(self, user_input=None):
#        # Manage the options for the integration.
#        # Example: allow users to update MQTT topic via UI
#        if user_input is not None:
#            # Validate and store options
#            return self.async_create_entry(title="", data=user_input)
#
#        options_schema = vol.Schema({
#            vol.Optional(
#                "mqtt_topic",
#                default=self.config_entry.options.get("mqtt_topic", "notification_catcher/default_topic")
#            ): str
#        })
#        return self.async_show_form(step_id="init", data_schema=options_schema)
