import RPi.GPIO as GPIO  # for Raspberry Pi
import epd2in7  # for e-ink display
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # IR receiver input
GPIO.setup(18, GPIO.OUT)  # IR emitter output
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 1 input (TV)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 2 input (DVD)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button 3 input (Audio)

# Set up e-ink display
epd = epd2in7.EPD()
epd.init()

# Define IR codes for your remote control devices
ir_codes = {
    #----- TV CODES -----#
    'TV_ON': [0x1234, 0x5678, 0x9012, 0x3456],  # example IR code for TV ON
    'TV_OFF': [0x9876, 0x5432, 0x1098, 0x7654],  # example IR code for TV OFF
    'DVD_ON': [0x1111, 0x2222, 0x3333, 0x4444],  # example IR code for DVD ON
    'DVD_OFF': [0x5555, 0x6666, 0x7777, 0x8888],  # example IR code for DVD OFF
    'AUDIO_ON': [0x9999, 0xAAAA, 0xBBBB, 0xCCCC],  # example IR code for Audio ON
    'AUDIO_OFF': [0xDDDD, 0xEEEE, 0xFFFF, 0x0000]  # example IR code for Audio OFF
}

def send_ir_code(code):
    # Send the IR code using the IR emitter
    GPIO.output(18, GPIO.HIGH)
    for pulse in code:
        GPIO.output(18, GPIO.LOW)
        time.sleep(pulse * 0.000001)  # adjust the sleep time as needed
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.000001)  # adjust the sleep time as needed
    GPIO.output(18, GPIO.LOW)

def display_options():
    # Clear the e-ink display
    epd.Clear(0xFF)

    # Display the device type options
    epd.DrawStr(10, 10, "Device Type:")
    epd.DrawStr(10, 30, "1. TV")
    epd.DrawStr(10, 50, "2. DVD")
    epd.DrawStr(10, 70, "3. Audio")

    # Update the e-ink display
    epd.display()

def display_selected_device(device):
    # Clear the e-ink display
    epd.Clear(0xFF)

    # Display the selected device
    epd.DrawStr(10, 10, "Selected Device:")
    epd.DrawStr(10, 30, device)

    # Update the e-ink display
    epd.display()

# Example usage:
while True:
    # Display the device type options
    display_options()

    # Check for button presses
    if GPIO.input(23) == GPIO.LOW:  # Button 1 (TV) pressed
        print("TV button pressed")
        send_ir_code(ir_codes['TV_ON'])
        display_selected_device("TV")
    elif GPIO.input(24) == GPIO.LOW:  # Button 2 (DVD) pressed
        print("DVD button pressed")
        send_ir_code(ir_codes['DVD_ON'])
        display_selected_device("DVD")
    elif GPIO.input(25) == GPIO.LOW:  # Button 3 (Audio) pressed
        print("Audio button pressed")
        send_ir_code(ir_codes['AUDIO_ON'])
        display_selected_device("Audio")

    # Wait for a short period before checking again
    time.sleep(0.1)
