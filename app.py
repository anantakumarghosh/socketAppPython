# app.py
import socket

HOST = 'localhost'  # The host where your Express.js server is running
PORT = 4000         # The port your Express.js socket server is listening on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to Express.js socket server')

    # Send data to the Express.js socket server
    message = "Hello from Python"
    print('Send: '+ message)
    s.sendall(message.encode())

    # Receive data from the Express.js socket server
    data = s.recv(1024)
    print('Received data from Express.js:', data.decode())

print('Connection closed')