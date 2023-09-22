import socket
import threading
import time

HOST = 'localhost'
PYTHON_PORT = 5000  # Python server port

# Function to handle incoming connections from Express.js
def handle_connection(connec, addr):
    print(f'Connected to Express.js at {addr}')

    while True:
        data = connec.recv(1024)
        if not data:
            break
        print(f'Received data from Express.js: {data.decode()}')

        # Process the data and send a response
        time.sleep(5)
        response = f"Response from Python: {data.decode()} 2"
        connec.sendall(response.encode())

    print(f'Connection closed with Express.js at {addr}')
    connec.close()

# Create a socket server to listen for connections from Express.js
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PYTHON_PORT))
    server_socket.listen()

    print('Python server is listening for connections from Express.js...')
    
    while True:
        connec, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(connec, addr))
        thread.start()
