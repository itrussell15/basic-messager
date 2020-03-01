from Messager import Messager
from gpiozero import Button
import time


url = "http://localhost:3000/message"
email = "message.reader15@gmail.com"
password = "zacisa12"
m = Messager(url, email, password)
button = Button(26)

#Main way of displaying the information that has been sent.
def display_message():

	queued = m.get_queued_message()
	print("Message from {}:\n\t{}".format(queued["author"], queued["body"])
	#Push message to the screen
	#push_to_screen(queued)

#Binds the "display_message" function to a button press -- need to test and make sure it will work even when inside of the loop
button.when_pressed = display_message

while True:
	

	m.push_new_messages()
	
	m.delete_old_messages()

	time.sleep(10)


#	m.push_new_messages()
#	queued = m.get_queued_message()
#	m.delete_old_messages()
#	print(queued)
#	time.sleep(1)
