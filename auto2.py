import pyautogui
import time
import webbrowser

# Function to open WhatsApp Web
def open_whatsapp_web():
    webbrowser.open("https://web.whatsapp.com")  # Open WhatsApp Web in the default browser
    print("Opening WhatsApp Web...")
    time.sleep(15)  # Wait for the page to load completely

# Function to activate WhatsApp Web and send a message
def activate_whatsapp_web(contact_name):
    # Give time to switch to the browser with WhatsApp Web open
    print("Switch to the browser with WhatsApp Web open in 5 seconds...")
    time.sleep(5)

    # Use Ctrl + Alt + / to open the search box
    pyautogui.hotkey('ctrl', 'alt', '/')  # This opens the search box in WhatsApp Web
    time.sleep(1)

    # Type the contact name
    pyautogui.write(contact_name)  # Type the contact's name
    time.sleep(2)  # Allow time for the contact to appear

    # Press enter to open the chat
    pyautogui.press('enter')
    time.sleep(2)  # Give time for the chat to open

# Function to send a message multiple times
def send_message():
    # Message details
    message = "Automated message"  # Message to send
    number_of_times = 5  # Number of times to send the message

    for i in range(number_of_times):
        pyautogui.write(message)  # Write the message in the message box
        pyautogui.press('enter')  # Press enter to send
        time.sleep(1)  # Wait before sending the next message

# Open WhatsApp Web and send messages
open_whatsapp_web()

# Use the contact name directly in the function
contact_name = "Trilochan ji"
activate_whatsapp_web(contact_name)
send_message()

print("Messages sent successfully!")
