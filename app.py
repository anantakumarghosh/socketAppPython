import socket
import threading
from flask import Flask, request

HOST = '127.0.0.1'  # System IP address
PYTHON_PORT = 5000  # Python Socket Listening port
PYTHON_FLASK_PORT = 5001 # Flask App server port
EXPRESS_HOST = '127.0.0.1'  # Express server's IP address
EXPRESS_PORT = 4000  # Express App Socket port
EXPRESS_SOCKET_PORT = 4000
app = Flask(__name__)

# Function to handle incoming connections from Express.js
def handle_connection(connec, addr):
    print(f'Connected to Express.js at {addr}')

    while True:
        data = connec.recv(1024)
        if not data:
            break
        print(f'Received data from Express.js: {data.decode()}')

        # Process the data and send a response
        response = f"{data.decode()} MODIFIED"
        print(f"I'm python, sending message back to Express socket: {response}")
        connec.sendall(response.encode())

    print(f'Connection closed with Express.js at {addr}')
    connec.close()

@app.route('/send', methods=['GET'])
def send_to_express():
    data = request.args.get('data')
    print(f"I'm Flask, Message sending to express socket: {data}")

    # Send the data to Express.js via socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((EXPRESS_HOST, EXPRESS_PORT))
        print(f'Connected to Express.js at {EXPRESS_HOST}:{EXPRESS_PORT}')
        client_socket.sendall(data.encode())

        # Receive the response from Express.js
        response = client_socket.recv(1024)
        responseData = response.decode()
        print(f'Received response from Express Socket Server: {responseData}')

    # Return the response with the received data
    response_message = f'Message sent to Express APP Socket successfully via GET request through Python socket: {data} \n Response: {responseData}'
    return response_message

# Create a socket server to listen for connections from Express.js
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PYTHON_PORT))
    server_socket.listen()

    print('Python server is listening for connections from Express.js...')

    def start_flask():
        app.run(host=HOST, port=PYTHON_FLASK_PORT)

    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    while True:
        connec, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(connec, addr))
        thread.start()
        thread.join()
