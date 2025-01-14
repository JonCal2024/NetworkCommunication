import socket
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

#Handle broadcasting from server
def broadcast_message(s, message):
    # Broadcast the message
    s.sendto(message.encode(), ('<broadcast>', 12345))
    # Whenever a message being sent
    logging.info("Message sent: %s", message[1:])

# Handle unicasting from server       
def unicast_message(s, message):
    # List of socket addresses that respond to verification message
    connected_sockets = []
        
    # Broadcast a connection verification message
    s.sendto("VConnection verification check".encode(), ('<broadcast>', 12345))
    
    # Record addresses of clients from incoming verification messages
    while True:
        try:
            data, addr = s.recvfrom(1024)
            analyze_received_data(data, addr, s)
            connected_sockets.append(addr)
        # Timeout after 0.5 seconds
        except socket.timeout:
            break
    
    # If connected_sockets is empty, return to main program
    if len(connected_sockets) <= 0:
        print("No connections")
        return
    
    # Display sockets that responded to verification for selection
    for index in range(len(connected_sockets)):
        print(f"{index + 1}. {connected_sockets[index]}")
    print("Which node would you like to unicast to? ", end="")
    
    # Error check input for unicast target selection
    while True:
        destination = input()
        if destination.isnumeric() and int(destination) > 0 and int(destination) <= len(connected_sockets):   
            break
        elif len(connected_sockets) > 0:
            print(f"\"{destination}\" must be an integer and in range, try again.")
    
    # Correct offset from display selection (display started at 1)
    destination = int(destination) - 1  
    # Unicast message to correct client
    s.sendto(message.encode(), (connected_sockets[destination][0], connected_sockets[destination][1]))
    # Whenever a message being sent
    logging.info("Message sent: %s", message[1:])

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
        elif flags == "B":
            cast_type = "Broadcast"
        else:
            cast_type = "Unknown"
        # Get source IP and port from passed address
        source_ip = source_addr[0]
        source_port = source_addr[1]
        # Determine destination IP and port from local socket
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
        
# Main function
def run_server():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((socket.gethostbyname('server'), 6969))
        # Enable broadcasting
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set response time to 0.5 seconds
        s.settimeout(0.5)
        
        while True:
            # Receive and validate user input    
            while True:
                print("Cast (B - Broadcast, U - Unicast, Q - close connection): ", end="")
                cast_type = input().upper().strip()
                if cast_type == "B" or cast_type == "U" or cast_type == "Q":
                    break
                else:
                    print(f"\"{cast_type}\" is invalid, try again.")
            
            # Prompt user for a message to send with cast
            print("Message: ", end="")
            # Message will have the cast_type as the first char, so client knows how to handle react
            message = cast_type + input()
            
            # If broadcast or close connection, broadcast message
            if cast_type == "B" or cast_type == "Q":
                broadcast_message(s, message)
                # If close connection, break out of loop and terminate
                if cast_type == "Q":
                    break
            # If unicast, call unicast function
            elif cast_type == "U":
                unicast_message(s, message)

if __name__ == "__main__":
    run_server()