import socket
import json

# Define the UDP broadcast address and port number
BROADCAST_IP = "0.0.0.0"
BROADCAST_PORT = 5001

# Create a UDP socket and bind it to the broadcast address and port
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_socket.bind((BROADCAST_IP, BROADCAST_PORT))

# Create the content dictionary
content_dictionary = {}

# Listen for UDP broadcast messages
while True:
    print("Listening for broadcast messages...")
    data, addr = udp_socket.recvfrom(1024)  # Receive data and the sender's address

    # Parse the received message as JSON
    try:
        message = json.loads(data.decode())
        filename = message.get('filename')
        chunk_names = message.get('chunks')

        # Update the content dictionary with the chunk names and sender's IP address
        for chunk_name in chunk_names:
            if chunk_name not in content_dictionary:
                content_dictionary[chunk_name] = []  # Use a list to store IP addresses
            if addr[0] not in content_dictionary[chunk_name]:
                content_dictionary[chunk_name].append(addr[0])  # Add the IP address to the list

        # Display the detected user (IP address) and their hosted content
        print(f"{addr[0]}: {', '.join(chunk_names)}")

        # Save the content dictionary to a shared text file
        with open("content_dictionary.txt", "w") as file:
            # Convert sets to lists before serializing to JSON
            content_dictionary_serializable = {
                chunk_name: list(ip_addresses)
                for chunk_name, ip_addresses in content_dictionary.items()
            }
            json.dump(content_dictionary_serializable, file)

    except json.JSONDecodeError:
        print("Invalid JSON format")

# Close the UDP socket
udp_socket.close()
