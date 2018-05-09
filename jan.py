# coding: utf-8

import json
import sys
from packet import Packet
from client_server import ClientServer

class Jan(ClientServer):
    def process_messages(self, connection, address):
        while True:
            data_json = connection.recv(1024)
            if not data_json: break
            data = json.loads(data_json.decode())
            self.log.debug('Message received from: '+data['actor'])
            self.message_received(data)
        connection.close()

    def message_received(self, message):
        self.log.debug('Message data: '+message['data'])

        if message['TER'] == True:
            self.log.debug('Terminating Communications...')
            sys.exit(0)

        if message['data'] == 'Execute':
            send = Packet(src_port=self.routes['Jan'], dest_port=self.routes['H'])
            send.data = 'HQ the enemy is located 32° 43’ 22.77” N,97° 9’ 7.53” W'
            send.URG = True
            send.auth_code = message['auth_code']
            deliverable = send.serialize().encode()
            self.sockets['H'].sendall(deliverable)

        self.log.debug('Returning acknowledgment')
        send = Packet()
        send.acknowledgement(message)
        send.actor = 'Jan'
        deliverable = send.serialize().encode()
        self.sockets['F'].sendall(deliverable)

    def send_message(self, message, destination):
        send = Packet(src_port=self.routes['Jan'], dest_port=self.routes[destination])
        send.data = message
        send.actor = 'Jan'

        if 'FIN' in message or message == 'Goodbye.':
            send.FIN = True
            send.TER = True

        if 'CONGRATULATIONS WE FRIED DRY GREEN LEAVES' in message:
            send.URG = True

        self.log.debug('Message from Jan to be delivered to '+destination)
        send.pretty_print()
        deliverable = send.serialize().encode()
        self.sockets['F'].sendall(deliverable)
