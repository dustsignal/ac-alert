# AC-Alert

AC-Alert is a Python script for monitoring aircraft data from a JSON file and sending alerts when a specific aircraft is detected.

## Overview

The script reads an `aircraft.json` file at a configurable interval, checking for a specific aircraft based on its hex code or flight registration number. When a target aircraft is found, it can trigger various types of alerts.

## Features

- **Email Alerts:** Send notifications via SMTP.
- **Sound Alerts:** Play a `.wav` or `.mp3` file.
- **Telegram Alerts:** Send messages to a Telegram chat.
- **Console Alerts:** Print messages to the console.
- **Styled Console Output:** Colored and formatted console output using the `rich` library.
- **Toggleable Console Output:** A master switch to turn all console output on or off.

## Installation

1.  **Clone the repository or download the files.**

2.  **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

    *This will install `requests`, `playsound`, and `rich`.*

## Configuration


All configuration is done in the `main.py` file. Open it and edit the following sections:

### General Configuration

- `AIRCRAFT_DATA_FILE`: The path to your aircraft data. This can be a local file path or a URL.
  - **Local File Example:** `'aircraft.json'`
  - **URL Example:** `'http://192.168.1.7/tar1090/data/aircraft.json'`
- `CHECK_INTERVAL`: The time in seconds between each check (default: `60`).

### Alerting Configuration

- `ALERT_ON_HEX`: The aircraft hex code to monitor (e.g., `'a835af'`).
- `ALERT_ON_FLIGHT`: The aircraft registration number to monitor (e.g., `'N628TS'`).

### Email Alert Configuration

- `EMAIL_ALERTS`: Set to `True` to enable email alerts.
- `SMTP_SERVER`: Your SMTP server address.
- `SMTP_PORT`: Your SMTP server port.
- `SMTP_USERNAME`: Your email username.
- `SMTP_PASSWORD`: Your email password.
- `EMAIL_SENDER`: The sender's email address.
- `EMAIL_RECIPIENT`: The recipient's email address.

### Sound Alert Configuration

- `SOUND_ALERTS`: Set to `True` to enable sound alerts.
- `SOUND_FILE_WAV`: The name of the `.wav` file to play (default: `'alert.wav'`).
- `SOUND_FILE_MP3`: The name of the `.mp3` file to play (default: `'alert.mp3'`).

### Telegram Alert Configuration

- `TELEGRAM_ALERTS`: Set to `True` to enable Telegram alerts.
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID.

### Console Configuration

- `CONSOLE_ALERTS`: Set to `True` to enable console alerts.
- `CONSOLE_OUTPUT`: A master switch to enable or disable all console output (default: `True`).

## Usage

To run the script manually:

```bash
python main.py
```

## Setting up as a Linux Service (systemd)

To run the script continuously as a service on a Linux system with systemd, follow these steps:

1.  **Create a service file:**

    ```bash
    sudo nano /etc/systemd/system/ac-alert.service
    ```

2.  **Add the following content to the file.** Make sure to replace `/path/to/your/project` with the absolute path to the project directory.

    ```ini
    [Unit]
    Description=AC-Alert - Aircraft Monitoring Script
    After=network.target

    [Service]
    User=your_user
    Group=your_group
    WorkingDirectory=/path/to/your/project
    ExecStart=/usr/bin/python3 /path/to/your/project/main.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

    *Replace `your_user` and `your_group` with your username and group (you can find these by running the `id` command).*

3.  **Reload systemd:**

    ```bash
    sudo systemctl daemon-reload
    ```

4.  **Enable the service to start on boot:**

    ```bash
    sudo systemctl enable ac-alert.service
    ```

5.  **Start the service:**

    ```bash
    sudo systemctl start ac-alert.service
    ```

6.  **Check the status of the service:**

    ```bash
    sudo systemctl status ac-alert.service
    ```

## Documentation

### `aircraft.json` Format

The script expects the `aircraft.json` file to have the following structure:

```json
{
    "aircraft": [
        {
            "hex": "a835af",
            "flight": "N628TS"
        },
        {
            "hex": "a4b2c3",
            "flight": "SWA123"
        }
    ]
}
```

### Alerting Functions

- `send_email(subject, body)`: Sends an email using the configured SMTP settings.
- `play_alert_sound()`: Plays the first sound file it finds (`.mp3` then `.wav`).
- `send_telegram_message(message)`: Sends a message via the Telegram Bot API.
- `log_to_console(message)`: Prints a message to the console.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
