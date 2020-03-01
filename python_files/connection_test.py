from Messager import Messager
import requests, json

url = "localhost:3000/message"
email = "itrussell15@gmail.com"
password = "zacisa12"

m = Messager(url, email, password)

#req = requests.get(url).json()
#print(req)

