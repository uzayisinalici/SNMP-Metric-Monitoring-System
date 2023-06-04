import time
import csv
from datetime import datetime
from threading import Thread
from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler
from pysnmp import debug


class SNMPMetricsServer:
    def __init__(self):
        self.clients = []
        self.running = False
        self.csv_headers = ['Timestamp', 'System Name', 'System Description', 'CPU Load']

    def add_client(self, client):
        self.clients.append(client)

    def start(self):
        self.running = True
        self._create_csv_files()

        # Create threads for each client
        threads = []
        for client in self.clients:
            thread = Thread(target=self._monitor_client, args=(client,))
            threads.append(thread)
            thread.start()

        # Start the server main loop
        while self.running:
            time.sleep(1)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    def stop(self):
        self.running = False

    def _create_csv_files(self):
        for client in self.clients:
            with open(client.file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.csv_headers)

    def _monitor_client(self, client):
        while self.running:
            metrics = self._get_metrics(client.ip_address, client.community_string)
            if metrics:
                self._save_metrics_to_csv(metrics, client.file_path)
            time.sleep(60)  # Wait for one minute

    def _get_metrics(self, device_ip, community_string):
        mib_builder = builder.MibBuilder()
        mib_path = mib_builder.getMibPath() + (".",)
        mib_view_controller = view.MibViewController(mib_builder)

        mib_builder.addMibSources(builder.DirMibSource(mib_path))
        mib_builder.loadModules("SNMPv2-MIB", "HOST-RESOURCES-MIB")

        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(community_string),
                   UdpTransportTarget((device_ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName')),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')),
                   ObjectType(ObjectIdentity('HOST-RESOURCES-MIB', 'hrProcessorLoad'))
                   )
        )

        if errorIndication:
            print('SNMP Error: %s' % errorIndication)
            return None

        if errorStatus:
            print('SNMP Error: %s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return None

        sys_name = varBinds[0][1].prettyPrint()
        sys_descr = varBinds[1][1].prettyPrint()
        cpu_load = varBinds[2][1].prettyPrint()

        metrics = {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'System Name': sys_name,
            'System Description': sys_descr,
            'CPU Load': cpu_load
        }

        return metrics

    def _save_metrics_to_csv(self, metrics, file_path):
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_headers)
            writer.writerow(metrics)


class SNMPClient:
    def __init__(self, ip_address, community_string, file_path):
        self.ip_address = ip_address
        self.community_string = community_string
        self.file_path = file_path


if __name__ == '__main__':
    server = SNMPMetricsServer()

    # Add clients with their IP addresses, community strings, and file paths
    client1 = SNMPClient('192.168.0.1', 'public', 'client1.csv')
    client2 = SNMPClient('192.168.0.2', 'public', 'client2.csv')

    server.add_client(client1)
    server.add_client(client2)

    # Start the SNMP server
    server.start()
