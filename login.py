import socket
import ssl
import json

#host = 88.205.102.20

login_data = ['xapib.x-station.eu', 5124, 10086262, "PASSWORD" ]

def xtbLogin(host, port, userId, password):

    # replace host name with IP, this should fail connection attempt,
    # but it doesn't in Python 2.x
    host = socket.getaddrinfo(host, port)[0][4][0]

    # create socket and connect to server
    # server address is specified later in connect() method
    sock = socket.socket()
    sock.connect((host, port))

    # wrap socket to add SSL support
    sock = ssl.wrap_socket(sock,
      # flag that certificate from the other side of connection is required
      # and should be validated when wrapping 
      cert_reqs=ssl.CERT_REQUIRED,
      # file with root certificates
      ca_certs="/home/stepan/scripts/cacert.pem"

    )

    #userId : 1002450, 1069924, 10086262

    packet = json.dumps({"command": "login", "arguments": {"userId": userId,"password": password,"appId": "test","appName": "test"}}, indent=4)

    sock.send(packet.encode("UTF-8"))
    return sock.recv(1280)

xtbLogin(*login_data)
