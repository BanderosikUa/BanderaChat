# Chat Websocket

Url path: ```ws://{server_ip}/chats/{chat_id}/ws```

### Send message(on send)
Need to send data to websocket with this format


action - 'send_message'

data:
- action
- message

example: ```{"action": "send_message", "message": "Hello world"}```


### Online status(on receive)
Receive data that user successfully has connected to websocket and now he is marked as online

action - 'online'

data:
- action
- user
- message
### Error status(on receive)
Receive data that some errors was occured with user or server

action - 'error'

data:
- action
- message


### Receive messsage(on receive)
Receive data that some user create message


action - 'newMessage'

data:
- action
- user
- message
- 
### Send ping(on send)
Send ping to handle ws open.

action - 'ping'

data:
- action

### Receive pong(on receive)
Receive pong from ws server that connection are alive

data:
- action("pong")
