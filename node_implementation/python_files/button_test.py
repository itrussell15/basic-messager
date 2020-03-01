from gpiozero import Button
import time

button = Button(26)
def print_nonsense():
	print("Non-Sense")

button.when_pressed = print_nonsense

while True:
	print("Sense")
	time.sleep(1)
