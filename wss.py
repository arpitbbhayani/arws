import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 5000))

# queue up as many as 5 connect requests (the normal max) before refusing outside connections
serversocket.listen(5)

server_response_400 = """HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=utf-8
Content-Length: 12

Bad Request
"""

server_response_wss = """HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
"""

while True:
    (clientsocket, address) = serversocket.accept()
    print("client connected on", address)

    # Client handshake request
    # The client will send a pretty standard HTTP request with headers that looks like this
    # (the HTTP version must be 1.1 or greater, and the method must be GET)
    #
    #
    # GET /socket.io/?EIO=4&transport=polling&t=Nl5IOYG HTTP/1.1
    # Host: localhost:5000
    # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
    # Accept: */*
    # Accept-Language: en-US,en;q=0.5
    # Accept-Encoding: gzip, deflate
    # Origin: http://localhost:5001
    # Connection: keep-alive
    # Referer: http://localhost:5001/
    # Sec-Fetch-Dest: empty
    # Sec-Fetch-Mode: cors
    # Sec-Fetch-Site: cross-site
    request = clientsocket.recv(1024).decode("utf-8")
    print(request)

    # When the server receives the handshake request, it should send back a
    # special response that indicates that the protocol will be changing
    # from HTTP to WebSocket.
    clientsocket.send(server_response_wss.encode('ascii'))


    clientsocket.close()
