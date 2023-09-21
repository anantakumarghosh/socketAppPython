# app.py
import socket

HOST = 'localhost'  # The host where your Express.js server is running
PORT = 4000         # The port your Express.js socket server is listening on

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('Connected to Express.js socket server')

        # Receive data from the Express.js socket server
        data = s.recv(1024)
        print('Received data from Express.js:', data.decode())

        # Modify the received data (e.g., add a prefix)
        modified_message = f"Modified by Python: {data.decode()}"

        # Send the modified message back to Express.js
        s.sendall(modified_message.encode())

    print('Connection closed')
