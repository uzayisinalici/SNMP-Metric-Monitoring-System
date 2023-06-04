import time
import csv
from datetime import datetime
from pysnmp.hlapi import *


class SNMPMetricsClient:
    def __init__(self, server_ip, server_port, community_string, file_path):
        self.server_ip = server_ip
        self.server_port = server_port
        self.community_string = community_string
        self.file_path = file_path

    def start(self):
        while True:
            metrics = self._get_metrics()
            if metrics:
                self._send_metrics(metrics)
            time.sleep(60)  # Wait for one minute

    def _get_metrics(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.community_string),
                   UdpTransportTarget((self.server_ip, self.server_port)),
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

    def _send_metrics(self, metrics):
        with open(self.file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=metrics.keys())
            writer.writerow(metrics)


if __name__ == '__main__':
    client = SNMPMetricsClient('192.168.0.10', 161, 'public', 'client.csv')
    client.start()
