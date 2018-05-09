import logging
import json
import sys
from packet import Packet
from client_server import ClientServer

class Chan(ClientServer):
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
            self.log.debug('CommunicationTerminated...')
            sys.exit(0)

        if message['ACK'] == True:
            self.log.debug('Acknowledgment received')
            return

        self.log.debug('Returning acknowledgment')
        send = Packet()
        send.acknowledgement(message)
        send.actor = 'Chan'
        send.pretty_print()
        deliverable = send.serialize().encode()
        self.sockets['E'].sendall(deliverable)

    def send_message(self, message, destination):
        send = Packet(src_port=self.routes['Chan'], dest_port=self.routes[destination])
        send.data = message
        send.actor = 'Chan'
        self.log.debug('Message from Chan to be delivered to '+destination)
        send.pretty_print()
        deliverable = send.serialize().encode()
        self.sockets['E'].sendall(deliverable)


