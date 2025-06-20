# Home Assistant Notification Catcher

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

A Home Assistant custom component to catch notifications sent via MQTT and display them as a sensor. This allows you to integrate notifications from various sources, like a Windows PC, into your Home Assistant setup for display or automation.

## Features

*   Listens to a specified MQTT topic for notification messages.
*   Creates a sensor entity in Home Assistant to display the latest notification.
*   Stores notification `title` and `message` as sensor attributes.
*   Timestamp of when the notification was received.

## Prerequisites

*   Home Assistant instance.
*   MQTT broker configured and integrated with Home Assistant (e.g., Mosquitto addon).
*   HACS installed (recommended for easy installation), or manual installation capability.

## Installation

### Option 1: HACS (Recommended)

1.  **Add Custom Repository:**
    *   Open HACS in Home Assistant.
    *   Go to "Integrations", then click the three dots in the top right and select "Custom repositories".
    *   In the "Repository" field, enter the URL of this GitHub repository.
    *   For "Category", select "Integration".
    *   Click "Add".
2.  **Install Component:**
    *   Search for "Notification Catcher" in HACS.
    *   Click "Install".
    *   Restart Home Assistant.

### Option 2: Manual Installation

1.  **Copy Files:**
    *   Download the `notification_catcher` directory from the `custom_components` directory of this repository.
    *   Copy the `notification_catcher` directory into your Home Assistant's `<config>/custom_components/` directory. If `custom_components` doesn't exist, create it.
2.  **Restart Home Assistant:**
    *   Restart your Home Assistant server to load the new component.

## Configuration

After installation (either via HACS or manually) and restarting Home Assistant:

1.  **Add Integration:**
    *   Go to **Settings > Devices & Services** in Home Assistant.
    *   Click **+ ADD INTEGRATION**.
    *   Search for "Notification Catcher" and select it.
    *   Follow the on-screen prompts. Since there are no configuration options in this version, it should be a simple confirmation step.
2.  **Sensor Creation:**
    *   Once added, a sensor entity named `sensor.last_notification` (or similar, depending on your entity naming conventions and if you rename it) will be created.
    *   This sensor listens to the hardcoded MQTT topic: `notification_catcher/notify`.

Your Home Assistant instance must have the MQTT integration configured and connected to your MQTT broker for this component to function.

## Sending Notifications

To send a notification to Home Assistant, you need to publish a JSON payload to the MQTT topic `notification_catcher/notify`.

**Payload Format:**
```json
{
  "title": "Your Notification Title",
  "message": "Your detailed notification message here."
}
```

**Example using `mosquitto_pub` (command-line MQTT client):**
```bash
mosquitto_pub -h YOUR_MQTT_BROKER_IP -p 1883 -u YOUR_MQTT_USERNAME -P YOUR_MQTT_PASSWORD -t "notification_catcher/notify" -m "{\"title\":\"Test Title\",\"message\":\"This is a test notification from my PC.\"}"
```
Replace `YOUR_MQTT_BROKER_IP`, `YOUR_MQTT_USERNAME`, and `YOUR_MQTT_PASSWORD` with your MQTT broker's details.

**Example using Python (paho-mqtt):**
```python
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.username_pw_set("YOUR_MQTT_USERNAME", "YOUR_MQTT_PASSWORD")
client.connect("YOUR_MQTT_BROKER_IP", 1883, 60)

payload = {
  "title": "From Python",
  "message": "Hello from a Python script!"
}

client.publish("notification_catcher/notify", json.dumps(payload))
client.disconnect()
```

## Displaying in Lovelace

You can display the notification sensor in your Lovelace dashboard using an Entities card or a custom card.

**Example Entities Card:**
```yaml
type: entities
entities:
  - entity: sensor.last_notification # Verify entity ID from Developer Tools > States
    name: Last Notification Received
  - entity: sensor.last_notification
    attribute: title
    name: Notification Title
  - entity: sensor.last_notification
    attribute: message
    name: Notification Message
  - entity: sensor.last_notification
    attribute: received_at
    name: Received At
```

## Future Enhancements (TODO)

*   Configurable MQTT topic via Home Assistant UI (ConfigFlow).
*   Ability to retain a list of notifications, not just the last one.
*   Service to clear notifications.
*   More detailed attributes (e.g., sender device).

---
*This is a basic custom component. Further development can add more features and flexibility.*
