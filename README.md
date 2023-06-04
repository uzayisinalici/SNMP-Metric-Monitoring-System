# SNMP Metric Monitoring System

The SNMP Metric Monitoring System is a Python-based solution for monitoring device metrics and system information using SNMP (Simple Network Management Protocol). 
The system consists of an SNMP server and SNMP clients, allowing you to monitor multiple devices and record the metrics at regular intervals.

## Features

- Retrieves device metrics and system information using SNMP protocol
- Supports HostResources MIB for CPU load, disk partitions, etc.
- Supports SNMPv2-MIB for system name, system description, hostname, etc.
- The server can serve multiple clients simultaneously
- Clients send metric requests every minute and record the results in CSV files

## Prerequisites

- Python 
- pysnmp library

## Installation

1. Clone the repository:

# SHELL
   git clone <repository_url>
Install the required dependencies:

# SHELL
Copy code
pip install pysnmp
Usage
SNMP Server
Open a terminal and navigate to the project directory.

Edit the server.py file to configure the SNMP server and clients:

Add SNMP clients by creating instances of the SNMPClient class with the appropriate IP address, community string, and file path for the CSV file.
Modify the server IP address, port, and community string if needed.
Start the SNMP server by running the following command:

# SHELL
Copy code
python server.py
SNMP Clients
Open a terminal and navigate to the project directory.

Edit the client.py file to configure the SNMP client:

Set the server IP address, port, community string, and file path for the CSV file.

Start the SNMP client by running the following command:

# SHELL
Copy code
python client.py

Repeat the above steps for each client you want to monitor.

# Customization
You can customize the SNMP metrics retrieved by modifying the get_metrics() function in server.py and client.py. 

Add or remove ObjectType entries as per your requirements.

The CSV file headers and structure can be modified by updating the csv_headers list in the SNMPMetricsServer class in server.py and the fieldnames parameter in the SNMPMetricsClient class in client.py.

