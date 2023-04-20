import socket
import threading

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_socket.bind(("localhost", 12345))

# Listen for incoming connections
server_socket.listen()

# Create a list to keep track of connected clients
clients = []

# Create a function to handle incoming connections
def handle_client(client_socket, client_address):
    # Add the client to the list of connected clients
    clients.append(client_socket)

    while True:
        try:
            # Receive a message from the client
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                # Broadcast the message to all connected clients
                for client in clients:
                    client.send(bytes(message, "utf-8"))
            else:
                # If an empty message is received, assume the client has disconnected
                client_socket.close()
                clients.remove(client_socket)
                break
        except:
            # If an error occurs, assume the client has disconnected
            client_socket.close()
            clients.remove(client_socket)
            break

# Create a function to accept incoming connections
def accept_connections():
    while True:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Create a thread to handle the new client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start accepting incoming connections
print("Server is listening for incoming connections...")
accept_connections()
