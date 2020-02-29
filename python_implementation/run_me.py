from Messager import Messager
from gpiozero import Button
import time

email = "message.reader15@gmail.com"
password = "zacisa12"
mes = Messager(email, password)

button = Button(26)
button.when_pressed = mes.process

while True:
	mes.messages_to_data()

	if mes.unread_message_count() > 0:
		mes.alert_user()

time.sleep(5)
