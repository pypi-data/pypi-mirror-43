# SimpleFbChat

Simple Facebook Chat library for students. Do not use at production.

Example:

```
from simplefbchat import SimpleFbChat

login = "example@tfbnw.net"
password = "passw0rd"

fb = SimpleFbChat(login, password)

while True:
    received_message = fb.receive()

    text = received_message.text

    received_message.reply("Hello: " + text)
```

