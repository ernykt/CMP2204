import socket
import json
import time
import os
from datetime import datetime

# Define the TCP server address and port number
SERVER_IP = "25.66.105.86"  # Replace with the actual server IP address
SERVER_PORT = 5000

# Define the directory where the chunk files are located
CHUNKS_DIRECTORY = r"C:\Users\musae\OneDrive\Masaüstü\sup"

# Create a TCP socket and listen for incoming connections
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((SERVER_IP, SERVER_PORT))
tcp_socket.listen()

print("Chunk Uploader is listening for connections...")

while True:
    # Accept a TCP connection request
    client_socket, client_address = tcp_socket.accept()

    try:
        # Receive the request message from the client
        request_message = client_socket.recv(1024).decode()

        # Parse the JSON message to determine the requested chunk
        parsed_message = json.loads(request_message)
        requested_chunk = parsed_message.get("requested_content")

        # Check if the requested chunk exists in the local directory
        filename = requested_chunk  # Append the file extension
        file_path = os.path.join(CHUNKS_DIRECTORY, filename)
        if requested_chunk and os.path.exists(file_path):
            # Open the file and read its contents
            with open(file_path, 'rb') as file:
                chunk_data = file.read()

            # Send the chunk data to the client
            client_socket.sendall(chunk_data)

            # Log the file's info in a text file
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = {
                'chunkname': requested_chunk,
                'timestamp': timestamp,
                'destinationIPaddress': client_address[0]
            }
            with open("upload_log.txt", 'a') as log_file:
                log_file.write(json.dumps(log_entry) + '\n')

            print(f"Chunk {requested_chunk} sent to {client_address[0]}")

    except json.JSONDecodeError:
        print("Invalid JSON message received.")
    except FileNotFoundError:
        print(f"Requested chunk {requested_chunk} does not exist.")
    finally:
        # Close the client socket
        client_socket.close()

# The Chunk Uploader service will persist and not terminate here
