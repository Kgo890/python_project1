import socket
import threading
import os
from datetime import datetime

# Constants
HOST = 'localhost'
PORT = 18000
MAX_USERS = 3
DOWNLOADS_DIR = "downloads"

# Ensure the downloads directory exists
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Server data structures
active_users = {}  # Format: {username: (socket, address)}
history = []       # Chat history with messages and timestamps

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender_socket=None):
    for username, (client_socket, _) in active_users.items():
        if client_socket != sender_socket:
            client_socket.sendall(message.encode())

# Function to handle each client
def handle_client(client_socket, client_address):
    username = None
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Parse and handle message based on command
            if message.startswith("JOIN_REQUEST"):
                username = message.split(":")[1]
                if username in active_users:
                    client_socket.send("JOIN_REJECT:The server rejects the join request. Another user is using this username.".encode())
                elif len(active_users) >= MAX_USERS:
                    client_socket.send("JOIN_REJECT:The server rejects the join request. The chatroom has reached its maximum capacity.".encode())
                else:
                    active_users[username] = (client_socket, client_address)
                    welcome_msg = f"Server: {username} joined the chatroom."
                    history.append(welcome_msg)
                    client_socket.send(f"JOIN_ACCEPT:The server welcomes you to the chatroom.\nType lowercase 'q' and press enter at any time to quit the chatroom.\nType lowercase 'a' and press enter at any time to upload an attachment to the chatroom.\nHere is a history of the chatroom.\n" + "\n".join(history).encode())
                    broadcast(f"{welcome_msg}", client_socket)

            elif message.startswith("QUIT_REQUEST"):
                quit_msg = f"Server: {username} left the chatroom."
                broadcast(quit_msg)
                if username in active_users:
                    del active_users[username]
                history.append(quit_msg)
                client_socket.send("QUIT_ACCEPT:You have left the chatroom.".encode())
                break

            elif message.startswith("MESSAGE"):
                msg_content = f"[{datetime.now().strftime('%H:%M:%S')}] {username}: {message.split(':', 1)[1]}"
                history.append(msg_content)
                broadcast(msg_content, client_socket)

            elif message.startswith("REPORT_REQUEST"):
                report = f"There are {len(active_users)} active users in the chatroom.\n" + "\n".join([f"{user} at IP: {addr[0]} and port: {addr[1]}" for user, (_, addr) in active_users.items()])
                client_socket.sendall(f"REPORT_RESPONSE:{report}".encode())

            elif message.startswith("ATTACHMENT"):
                filename = message.split(":")[1]
                file_content = client_socket.recv(4096)
                file_path = os.path.join(DOWNLOADS_DIR, os.path.basename(filename))
                with open(file_path, 'wb') as f:
                    f.write(file_content)
                attachment_msg = f"[{datetime.now().strftime('%H:%M:%S')}] {username} sent an attachment: {filename}"
                history.append(attachment_msg)
                broadcast(attachment_msg, client_socket)
                for client in active_users.values():
                    client[0].sendall(f"Attachment received: {filename}\nContent:\n{file_content.decode()}".encode())

        except Exception as e:
            print(f"Error handling message from {username}: {e}")
            break

    if username in active_users:
        del active_users[username]
    client_socket.close()

# Main function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
