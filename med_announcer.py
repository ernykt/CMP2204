import os
import math
import socket
import json
import time

# Define the UDP broadcast address and port number
BROADCAST_IP = '255.255.255.255'
BROADCAST_PORT = 5001

def divide_file_into_chunks(filename, content_name):
    c = os.path.getsize(filename)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)

    chunk_names = []
    index = 1
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunk_name = f"{content_name}_{index}"
            with open(chunk_name, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            chunk_names.append(chunk_name)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))

    return chunk_names

def send_broadcast_message(chunk_names, file_to_host):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        message = {
            'filename': file_to_host,
            'chunks': chunk_names
        }
        json_message = json.dumps(message)
        udp_socket.sendto(json_message.encode(), (BROADCAST_IP, BROADCAST_PORT))
        print("Announcement sent")
        time.sleep(60)

def chunk_announcer():
    # Ask the user to specify the file to initially host
    file_to_host = input("Enter the file name to host: ")
    content_name = os.path.splitext(file_to_host)[0]

    # Divide the specified file into chunks
    chunk_names = divide_file_into_chunks(file_to_host, content_name)

    # Display the number of chunks
    print(f"Number of chunks: {len(chunk_names)}")

    # Start sending broadcast messages periodically
    send_broadcast_message(chunk_names, file_to_host)
    

if __name__ == "__main__":
    chunk_announcer()
write every ip adress once