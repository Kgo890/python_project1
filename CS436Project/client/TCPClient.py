import socket
import threading
import os

# Constants
SERVER_HOST = 'localhost'
SERVER_PORT = 18000
ATTACHMENTS_DIR = "attachments"
DOWNLOADS_DIR = "downloads"

# Ensure directories exist
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Error receiving message.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        print("Menu:\n1. Get a report of the chatroom from the server.\n2. Request to join the chatroom.\n3. Quit the program.\nChoice:", end=" ")
        choice = input().strip()

        if choice == "1":
            client_socket.send("REPORT_REQUEST".encode())

        elif choice == "2":
            username = input("Please enter a username: ")
            client_socket.send(f"JOIN_REQUEST:{username}".encode())

        elif choice == "3":
            client_socket.send("QUIT_REQUEST".encode())
            print("You left the chatroom.")
            break

        elif choice == "a":  # Upload a file
            filename = input("Please enter the file path and name (from 'attachments' folder): ")
            filepath = os.path.join(ATTACHMENTS_DIR, filename)
            if os.path.isfile(filepath):
                client_socket.send(f"ATTACHMENT:{filename}".encode())
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                    client_socket.sendall(file_data)
                print("File sent successfully.")
            else:
                print("File not found in attachments folder.")

        else:
            print("Invalid choice.")

    client_socket.close()

if __name__ == "__main__":
    start_client()
