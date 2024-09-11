import machine
import utime
from ssd1306 import SSD1306_I2C

# Pin configuration
IR_LED_PIN = 15
UP_BUTTON_PIN = 0
DOWN_BUTTON_PIN = 1
LEFT_BUTTON_PIN = 2
RIGHT_BUTTON_PIN = 3
SELECT_BUTTON_PIN = 4

# Initialize display (I2C address might be different)
i2c = machine.I2C(1, scl=machine.Pin(5), sda=machine.Pin(4))
display = SSD1306_I2C(128, 64, i2c)

# Initialize pins
ir_led = machine.Pin(IR_LED_PIN, machine.Pin.OUT)
up_button = machine.Pin(UP_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
down_button = machine.Pin(DOWN_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
left_button = machine.Pin(LEFT_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
right_button = machine.Pin(RIGHT_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
select_button = machine.Pin(SELECT_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Configuration dictionary for IR codes
DEVICE_IR_CODES = {
    'TV': {
        'Sony': {
            'Model1': {
                'Power': 0x1A,
                'VolumeUp': 0x2B,
                'VolumeDown': 0x3C,
                'ChannelUp': 0x4D,
                'ChannelDown': 0x5E,
                'Mute': 0x6F,
                'Input': 0x7A,
                'Menu': 0x8B
            },
            'Model2': {
                'Power': 0x9C,
                'VolumeUp': 0xAD,
                'VolumeDown': 0xBE,
                'ChannelUp': 0xCF,
                'ChannelDown': 0xDE,
                'Mute': 0xEF,
                'Input': 0xF0,
                'Menu': 0xF1
            }
        },
        'Samsung': {
            'Model1': {
                'Power': 0xAA,
                'VolumeUp': 0xBB,
                'VolumeDown': 0xCC,
                'ChannelUp': 0xDD,
                'ChannelDown': 0xEE,
                'Mute': 0xFF,
                'Input': 0x00,
                'Menu': 0x11
            }
        }
    },
    'DVD': {
        'LG': {
            'Model1': {
                'Play': 0x1A,
                'Pause': 0x2B,
                'Stop': 0x3C,
                'Rewind': 0x4D,
                'FastForward': 0x5E,
                'NextTrack': 0x6F,
                'PrevTrack': 0x7A,
                'Eject': 0x8B
            }
        }
    }
}

# Global state
menu_level = 0
selected_option = 0
device = None
brand = None
model = None

def send_ir_code(code):
    # Implement IR sending logic here
    ir_led.value(1)  # Turn on IR LED
    # Send the IR code here (implementation depends on IR library)
    utime.sleep(0.1)  # Adjust timing as needed
    ir_led.value(0)  # Turn off IR LED

def display_menu(options, selected_index):
    display.fill(0)  # Clear display
    for i, option in enumerate(options):
        if i == selected_index:
            display.text("> " + option, 0, i * 10)  # Highlight selected option
        else:
            display.text(option, 0, i * 10)
    display.show()

def main():
    global menu_level, selected_option, device, brand, model

    while True:
        if menu_level == 0:
            options = ['TV', 'DVD']
            display_menu(options, selected_option)
            if not up_button.value():
                selected_option = (selected_option - 1) % len(options)
                utime.sleep(0.2)
            if not down_button.value():
                selected_option = (selected_option + 1) % len(options)
                utime.sleep(0.2)
            if not select_button.value():
                if selected_option == 0:
                    device = 'TV'
                else:
                    device = 'DVD'
                menu_level = 1
                selected_option = 0
                utime.sleep(0.2)
        
        elif menu_level == 1:
            brands = list(DEVICE_IR_CODES[device].keys())
            display_menu(brands, selected_option)
            if not up_button.value():
                selected_option = (selected_option - 1) % len(brands)
                utime.sleep(0.2)
            if not down_button.value():
                selected_option = (selected_option + 1) % len(brands)
                utime.sleep(0.2)
            if not select_button.value():
                brand = brands[selected_option]
                menu_level = 2
                selected_option = 0
                utime.sleep(0.2)
        
        elif menu_level == 2:
            models = list(DEVICE_IR_CODES[device][brand].keys())
            display_menu(models, selected_option)
            if not up_button.value():
                selected_option = (selected_option - 1) % len(models)
                utime.sleep(0.2)
            if not down_button.value():
                selected_option = (selected_option + 1) % len(models)
                utime.sleep(0.2)
            if not select_button.value():
                model = models[selected_option]
                menu_level = 3
                selected_option = 0
                utime.sleep(0.2)
        
        elif menu_level == 3:
            buttons = list(DEVICE_IR_CODES[device][brand][model].keys())
            display_menu(buttons, selected_option)
            if not up_button.value():
                selected_option = (selected_option - 1) % len(buttons)
                utime.sleep(0.2)
            if not down_button.value():
                selected_option = (selected_option + 1) % len(buttons)
                utime.sleep(0.2)
            if not select_button.value():
                button_name = buttons[selected_option]
                ir_code = DEVICE_IR_CODES[device][brand][model][button_name]
                send_ir_code(ir_code)
                utime.sleep(0.2)
            if not left_button.value():
                menu_level = 2
                selected_option = 0
                utime.sleep(0.2)
            if not right_button.value():
                menu_level = 0
                selected_option = 0
                device = None
                brand = None
                model = None
                utime.sleep(0.2)

if __name__ == "__main__":
    main()
