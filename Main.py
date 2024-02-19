import machine
import time

# Define the GPIO pins for the buttons and LEDs
start_button_pin = 16
pause_button_pin = 17
reset_button_pin = 18
led1_pin = 14
led2_pin = 15

# Initialize the GPIO pins
start_button = machine.Pin(start_button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
pause_button = machine.Pin(pause_button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
reset_button = machine.Pin(reset_button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
led1 = machine.Pin(led1_pin, machine.Pin.OUT)
led2 = machine.Pin(led2_pin, machine.Pin.OUT)

# Initialize the state
led_state = 0  # 0 for off, 1 for led1, 2 for led2
is_flashing = False
start_time = 0

# Function to alternate LEDs
def alternate_leds():
    global led_state, is_flashing, start_time
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 60000:  # Run for 1 minute
        if is_flashing:
            if led_state == 1:
                led1.value(1)
                led2.value(0)
                time.sleep(0.5)
                led_state = 2
            else:
                led1.value(0)
                led2.value(1)
                time.sleep(0.5)
                led_state = 1
        else:
            break
    led1.value(0)
    led2.value(0)

# Start button interrupt handler
def start_button_pressed(pin):
    global is_flashing
    if not is_flashing:
        is_flashing = True
        alternate_leds()

# Pause button interrupt handler
def pause_button_pressed(pin):
    global is_flashing
    if is_flashing:
        is_flashing = False

# Reset button interrupt handler
def reset_button_pressed(pin):
    global is_flashing
    if is_flashing:
        is_flashing = False
    led1.value(0)
    led2.value(0)

# Configure interrupts for the buttons
start_button.irq(trigger=machine.Pin.IRQ_RISING, handler=start_button_pressed)
pause_button.irq(trigger=machine.Pin.IRQ_RISING, handler=pause_button_pressed)
reset_button.irq(trigger=machine.Pin.IRQ_RISING, handler=reset_button_pressed)

# Main loop (do nothing in the main loop)
while True:
    pass
