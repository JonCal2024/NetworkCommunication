# Distributed Network Systems Project
by: Kirby James Fernandez
	Jonny Olswang
	Joshua Reyes

## Introduction
This project aims to analyze network communications by monitoring and logging details of all communications. The project includes scripts for broadcasting and unicasting messages, receiving messages, and analyzing network packets. It leverages Docker for containerization and networking, and Python for scripting.

## Features
- **Broadcast Messages:** The `master.py` script broadcasts messages to all nodes in the network.
- **Unicast Messages:** The `master.py` script unicasts messages to any node in the network.
- **Receive Messages:** The `node.py` script listens for messages broadcasted by the master. The `master.py` script listens for certain return messages from the nodes.
- **Network Analysis:** The scripts log detailed information about communications.
- **Docker Support:** All scripts can be containerized using Docker, making it easy to deploy and run on any system with Docker installed.

## Prerequisites
- **Docker:** To build and run the project containers.
- **Python:** For script execution.

## Installation

### Installing Docker
Follow the official Docker documentation to install Docker on your system.
[Docker Installation Guide](https://docs.docker.com/get-docker/)

### Building Docker Images and Containers
1. **Navigate to the Project Directory:** Open a terminal and navigate to the root directory of your project.
Proj1
  |
  +-----master
  |       |
  |       +--Dockerfile
  |       +--master.py`
  |       +--requirements.txt
  |
  +-----nodes
  |       |
  |       +--__pycache__
  |       +--Dockerfile
  |       +--node.py`
  |       +--requirements.txt
  |
  +--network_data.txt
   
2. **Build the Docker Images:**
In 'master' folder, run:
```
docker build -t master-server .
```
In 'nodes' folder, run:
```
docker build -t node .
```
3. **Run the Containers:**
```
docker run -it -v /abs/path:/app/data --net=Proj1-distributed-network --name=server master_server
docker run -it -v /abs/path:/app/data --net=Proj1-distributed-network --name=n0 node
docker run -it -v /abs/path:/app/data --net=Proj1-distributed-network --name=n1 node
docker run -it -v /abs/path:/app/data --net=Proj1-distributed-network --name=n2 node
docker run -it -v /abs/path:/app/data --net=Proj1-distributed-network --name=n3 node
```
Replace /abs/path with the absolute path to the directory where you wish to store your network_data.txt file

-it: runs the containers in interactive mode
-v (-volume): maps a path in the container to an absolute path in the host machine for the sake of persisting data
--net: specify a Docker network to run container on
--name: specify a name for the Docker container

## Testing
### Testing Master and Node Scripts
1. **Start the master_server Container:**
```
docker start server
```
2. **Start the node Containers:**
```
docker start n0 n1 n2 n3
```
3. **Check Logs:** To verify that messages are being sent and received, check the logs of the master_server and node containers:
```
docker logs server
docker logs n0
docker logs n1
docker logs n2
docker logs n3
```

## Configuring Firewall and Enabling Ports
To ensure that your network analysis scripts can communicate effectively, you may need to configure your firewall to allow traffic on specific ports. The exact steps depend on your operating system and firewall software. Generally, you would need to add rules to allow incoming and outgoing traffic on the ports used by your scripts.

## References
- [Docker Documentation](https://docs.docker.com/)

##
This project is open-source intended for Networks and Distributed Systems

