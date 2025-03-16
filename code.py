import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008

# Create the I2C bus with a frequency of 400 kHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mcp = MCP23008(i2c)

# Set up buttons on pins 0 through 3 with pull-ups
buttons = []
for pin in range(4):
    button = mcp.get_pin(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

print("Monitoring buttons on MCP23008...")

while True:
    for i, button in enumerate(buttons):
        try:
            # With pull-ups, a pressed button reads as False (0)
            if not button.value:
                print("Button on MCP23008 pin {} pressed.".format(i))
                # Reduced debounce: wait until button is released, checking every 5 ms
                while not button.value:
                    time.sleep(0.005)
        except OSError as e:
            # Ignore OSError 19 ("No such device") and continue.
            if e.errno == 19:
                pass  # Simply ignore this error.
            else:
                raise  # Re-raise unexpected errors.
    time.sleep(0.1)
