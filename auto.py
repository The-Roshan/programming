import pywhatkit
import time

# Define the phone number and the message
phone_number = '+916204469651'  # Replace with the recipient's phone number
message = 'This is an automated message'

# Define the time to start sending (current or in the future)
hour = 12  # Hour to start sending the first message (24-hour format)
minute = 52  # Minute to start sending the first message

# Number of messages to send
num_messages = 5

# Delay between messages in seconds
delay_between_messages = 1  # 1-minute delay between messages

# Send multiple messages
for i in range(num_messages):
    # Send the message
    print(f"Sending message {i+1} to {phone_number}")
    pywhatkit.sendwhatmsg(phone_number, f"{message} {i+1}", hour, minute)
    
    # Update the time for the next message
    minute += 2  # Increment the minute (make sure it doesn't exceed 59)

    # Wait before sending the next message (ensuring there's a delay)
    time.sleep(delay_between_messages)
