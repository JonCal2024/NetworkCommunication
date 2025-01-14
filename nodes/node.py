import socket
import threading
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Send network message information to a file
def analyze_received_data(data, source_addr, recv_socket):
    # Write to a file in docker container, which will be mapped with docker volume to another location on host
    with open("/app/data/network_data.txt", 'a') as f:
        # Record time recieved
        time = datetime.now()
        # No standard flags for UDP, will use custom flags stored in first char of message
        flags = data.decode()[0]
        if flags == "U":
            cast_type = "Unicast"
        elif flags == "B" or flags == "V" or flags == "Q":
            cast_type = "Broadcast"
        else:
            cast_type = "Unknown"
        # Get source IP and port from passed address
        source_ip = source_addr[0]
        source_port = source_addr[1]
        # Determine destination IP and port from local socket
        # Sockets of nodes are not bound, so they will display IP as 0.0.0.0 (listening to all interfaces)
        destination_ip = recv_socket.getsockname()[0]
        destination_port = recv_socket.getsockname()[1]
        # Determine if local socket is UPD or TCP
        if recv_socket.type == socket.SOCK_DGRAM:
            protocol = "UDP"
        elif recv_socket.type == socket.SOCK_STREAM:
            protocol = "TCP"
        else:
            protocol = "Unknown"
        # Length of sent message
        length = len(data)
        
        f.write(f"Type: {cast_type} | Time: {time} | Source IP: {source_ip} | Destination IP: {destination_ip} | Source Port: {source_port} | Destination Port: {destination_port} | Protocol: {protocol} | Length: {length} | Flags: {flags}\n")

def receive_messages():
    #Start listening for messages and log them.
    
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Bind to all interfaces
            s.bind(('', 12345))
            logging.info("Starting to receive messages...")
            while True:
                # Wait for a message
                data, addr = s.recvfrom(1024)
                analyze_received_data(data, addr, s)
                message = data.decode()
                logging.info("Received message: %s from %s", message[1:], addr)
                
                # If message is a broadcast
                if message[0] == "B":
                    print(f"Received broadcast: \"{message[1:]}\" from {addr}")
                # If message is a closing connection request, break out of loop and terminate
                elif message[0] == "Q":
                    print(f"Received closing request: \"{message[1:]}\" from {addr}")
                    break
                # If message is a unicast
                elif message[0] == "U":
                    print(f"Received unicast: \"{message[1:]}\" from {addr}")
                # If message is a headcount verification request
                elif message[0] == "V":
                    # Send back a unicast verification message to the server
                    s.sendto("UI'm connected".encode(), (addr[0],addr[1]))
                    
                # Example task: print the message
                print(f"Task: Processing message \"{message[1:]}\" from {addr}")
        except Exception as e:
            logging.error("Error receiving message: %s", e)

if __name__ == "__main__":
    # Start the message receiving thread
    threading.Thread(target=receive_messages).start() 