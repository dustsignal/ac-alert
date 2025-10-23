import json
import time
import smtplib
import os
import requests
from playsound import playsound
import platform
from rich.console import Console

# --- CONFIGURATION ---
AIRCRAFT_DATA_FILE = 'PATH_TO_YOUR_AIRCRAFT_JSON_FILE_OR_URL/aircraft.json'
CHECK_INTERVAL = 60  # seconds

# --- Alerting Configuration ---
ALERT_ON_FLIGHT = 'N712JM'  # e.g., 'N628TS'
# ALERT_ON_HEX = 'a240dc'  # e.g., 'a835af'

# --- Email Alert Configuration ---
EMAIL_ALERTS = False # Enable or disable email alerts
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_email_password'
EMAIL_SENDER = 'your_email@example.com'
EMAIL_RECIPIENT = 'recipient_email@example.com'

# --- Sound Alert Configuration ---
SOUND_ALERTS = True # Enable or disable sound alerts
SOUND_FILE_WAV = 'alert.wav'
# SOUND_FILE_MP3 = 'chime.mp3'

# --- Telegram Alert Configuration ---
TELEGRAM_ALERTS = False # Enable or disable Telegram alerts
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

# --- Console Configuration ---
CONSOLE_ALERTS = True # Enable or disable console alerts
CONSOLE_OUTPUT = True  # Master switch for all console output

# --- INITIALIZATION ---
console = Console()

# --- FUNCTIONS ---

def send_email(subject, body):
    """Sends an email alert."""
    if not EMAIL_ALERTS:
        return

    try:
        message = f"Subject: {subject}\n\n{body}"
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, message)
        if CONSOLE_OUTPUT: console.print("[green]Email alert sent successfully.[/green]")
    except Exception as e:
        if CONSOLE_OUTPUT: console.print(f"[red]Failed to send email alert: {e}[/red]")

def play_alert_sound():
    """Plays a sound alert."""
    if not SOUND_ALERTS:
        return

    sound_file_to_play = None
    if os.path.exists(SOUND_FILE_MP3):
        sound_file_to_play = SOUND_FILE_MP3
    elif os.path.exists(SOUND_FILE_WAV):
        sound_file_to_play = SOUND_FILE_WAV

    if sound_file_to_play:
        try:
            playsound(sound_file_to_play)
            if CONSOLE_OUTPUT: console.print("[green]Sound alert played successfully.[/green]")
        except Exception as e:
            if CONSOLE_OUTPUT: console.print(f"[red]Failed to play sound alert: {e}[/red]")
    else:
        if CONSOLE_OUTPUT: console.print("[yellow]No sound file found (alert.mp3 or alert.wav).[/yellow]")


def send_telegram_message(message):
    """Sends a message to a Telegram chat."""
    if not TELEGRAM_ALERTS:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {{'chat_id': TELEGRAM_CHAT_ID, 'text': message}}
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            if CONSOLE_OUTPUT: console.print("[green]Telegram message sent successfully.[/green]")
        else:
            if CONSOLE_OUTPUT: console.print(f"[red]Failed to send Telegram message. Status code: {response.status_code}[/red]")
    except Exception as e:
        if CONSOLE_OUTPUT: console.print(f"[red]Failed to send Telegram message: {e}[/red]")

def log_to_console(message):
    """Prints a message to the console."""
    if not CONSOLE_ALERTS or not CONSOLE_OUTPUT:
        return
    
    console.print(f"[bold cyan]CONSOLE ALERT:[/] {message}")


def check_aircraft_data():
    """Reads aircraft data and triggers alerts if a target is found."""
    try:
        if AIRCRAFT_DATA_FILE.startswith('http://') or AIRCRAFT_DATA_FILE.startswith('https://'):
            response = requests.get(AIRCRAFT_DATA_FILE)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
        else:
            with open(AIRCRAFT_DATA_FILE, 'r') as f:
                data = json.load(f)
    except FileNotFoundError:
        if CONSOLE_OUTPUT: console.print(f"[red]Error: '{AIRCRAFT_DATA_FILE}' not found.[/red]")
        return
    except requests.exceptions.RequestException as e:
        if CONSOLE_OUTPUT: console.print(f"[red]Error fetching data from URL: {e}[/red]")
        return
    except json.JSONDecodeError:
        if CONSOLE_OUTPUT: console.print(f"[red]Error: Could not decode JSON from '{AIRCRAFT_DATA_FILE}'.[/red]")
        return

    aircraft_list = data.get('aircraft', [])
    if not isinstance(aircraft_list, list):
        if CONSOLE_OUTPUT: console.print(f"[red]Error: JSON in '{AIRCRAFT_DATA_FILE}' is not in the expected format (missing 'aircraft' list).[/red]")
        return

    for aircraft in aircraft_list:
        hex_code = aircraft.get('hex', '').strip().lower()
        flight = aircraft.get('flight', '').strip().upper()

        if (ALERT_ON_HEX and hex_code == ALERT_ON_HEX.lower()) or \
           (ALERT_ON_FLIGHT and flight == ALERT_ON_FLIGHT.upper()):
            
            alert_message = f"Aircraft {ALERT_ON_HEX or ALERT_ON_FLIGHT} detected!"
            if CONSOLE_OUTPUT: console.print(f"[bold magenta]Aircraft {ALERT_ON_HEX or ALERT_ON_FLIGHT} detected![/bold magenta]")

            # Trigger alerts
            log_to_console(alert_message)
            send_email("Aircraft Alert", alert_message)
            play_alert_sound()
            send_telegram_message(alert_message)
            
            # Optional: Stop after first detection in a cycle
            return 

# --- MAIN LOOP ---
if __name__ == "__main__":
    if CONSOLE_OUTPUT: console.print("[bold blue]Starting AC-Alert monitoring...[/bold blue]")
    while True:
        check_aircraft_data()
        if CONSOLE_OUTPUT: console.print(f"[dim]Waiting for {CHECK_INTERVAL} seconds...[/dim]")
        time.sleep(CHECK_INTERVAL)
