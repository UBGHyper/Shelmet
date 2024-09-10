import RPi.GPIO as GPIO
import time
import epd2in7  # import the epd library for 2.7" E Ink display

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # IR receiver input
GPIO.setup(18, GPIO.OUT)  # IR emitter output

# Initialize the E Ink display
epd = epd2in7.EPD()
epd.init()

# Define IR codes for your remote control devices
ir_codes = {
    'TV_ON': [0x1234, 0x5678, 0x9012, 0x3456],  # example IR code for TV ON
    'TV_OFF': [0x9876, 0x5432, 0x1098, 0x7654]  # example IR code for TV OFF
}

captured_codes = []  # store captured IR codes
present_codes = ir_codes.copy()  # store present IR codes

def send_ir_code(code):
    # Send the IR code using the IR emitter
    GPIO.output(18, GPIO.HIGH)
    for pulse in code:
        GPIO.output(18, GPIO.LOW)
        time.sleep(pulse * 0.000001)  # adjust the sleep time as needed
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.000001)  # adjust the sleep time as needed
    GPIO.output(18, GPIO.LOW)

def receive_ir_code():
    # Receive the IR code using the IR receiver
    code = []
    while True:
        if GPIO.input(17) == GPIO.HIGH:
            start_time = time.time()
            while GPIO.input(17) == GPIO.HIGH:
                pass
            pulse_width = time.time() - start_time
            code.append(pulse_width)
        else:
            break
    return code

def display_codes():
    # Clear the E Ink display
    epd.Clear(0xFF)
    
    # Display captured IR codes
    epd.text("Captured Codes:", 0, 0, epd.get_font('Font12'))
    for i, code in enumerate(captured_codes):
        epd.text(f"{i+1}. {code}", 0, 20 + i * 20, epd.get_font('Font12'))
    
    # Display present IR codes
    epd.text("Present Codes:", 0, 120, epd.get_font('Font12'))
    for i, (name, code) in enumerate(present_codes.items()):
        epd.text(f"{i+1}. {name} - {code}", 0, 140 + i * 20, epd.get_font('Font12'))
    
    # Update the E Ink display
    epd.display(epd.get_buffer(epd.width, epd.height))

# Example usage:
while True:
    # Receive an IR code from the remote control
    received_code = receive_ir_code()
    print("Received IR code:", received_code)
    
    # Check if the received code matches a known IR code
    for name, code in ir_codes.items():
        if received_code == code:
            print("Matched IR code:", name)
            # Perform the corresponding action (e.g., send the IR code back)
            send_ir_code(code)
            break
    else:
        # If no match, add the received code to the captured codes list
        captured_codes.append(received_code)
        print("New IR code captured!")
    
    # Update the display
    display_codes()
    time.sleep(1)  # update the display every 1 second
