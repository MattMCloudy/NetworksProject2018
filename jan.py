# coding: utf-8

import json
from packet import Packet
from client_server import ClientServer

class Jan(ClientServer):
    def process_messages(self, connection, address):
        while True:
            data_json = connection.recv(1024)
            if not data: break
            data = json.loads(data_json.decode())
            self.log.debug('Message received from: '+data['actor'])
            self.message_received(data)
        connection.close()

    def message_received(self, message):
        self.log.debug('Message data: '+message['data'])

        if message['data'] == 'Execute':
            send = Packet(src_port=self.routes['Jan'], dest_port=self.routes['H'])
            send.data = 'HQ the enemy is located 32° 43’ 22.77” N,97° 9’ 7.53” W'
            send.URG = True
            send.auth_code = message['auth_code']
            deliverable = send.serialize().encode()
            self.sockets['H'].sendall(deliverable)