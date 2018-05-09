# coding: utf-8

import json
import sys
from packet import Packet
from client_server import ClientServer

class Ann(ClientServer):
    def __init__(self, name, args):
        super(Ann, self).__init__(name=name, args=args)
        self.chan_termination = 6

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

        if message['actor'] == 'Chan':
            self.chan_termination -= 1
            if self.chan_termination <= 0:
                message['RST'] = True
        elif message['FIN'] == True or message['data'] == 'Okay Goodbye' or 'FIN' in message['data']:
            self.log.debug('Ann connection terminated')
            sys.exit(0)

        #Send new packet in response
        send = Packet(src_port=self.routes['Ann'], dest_port=self.routes[message['actor']])

        #Connection with Chan to be terminated
        if message['RST'] == True and self.chan_termination <= 0:
            self.log.debug('Terminating connection with Chan...')
            send.data = 'TER'
            send.actor = 'Ann'
            send.TER = True
            send.RST = True
            deliverable = send.serialize().encode()
            self.log.debug('Sending packet to Router A')
            self.sockets['A'].sendall(deliverable)
        else:
            #Acknowledge packet, check for urgent phrases, accept message input
            send.acknowledgement(message)
            self.log.debug('Returning acknowledgment')

            if '32° 43’ 22.77” N,97° 9’ 7.53” W' in message['data']:
                send.URG = True
                send.auth_code = 'PEPPER THE PEPPER'

            if 'CONGRATULATIONS WE FRIED DRY GREEN LEAVES' in message['data']:
                send.URG = True
                send.data = 'Congrats Meet me at this location: 32.76” N, -97.07” W'
            else:
                send.data = input('What is your message: ')

            send.actor = 'Ann'
            self.log.debug('Sending packet to Router A')
            send.pretty_print()
            deliverable = send.serialize().encode()
            self.sockets['A'].sendall(deliverable)

    def send_message(self, message, destination):
        send = Packet(src_port=self.routes['Ann'], dest_port=self.routes[destination])
        send.data = message
        send.actor = 'Ann'
        self.log.debug('Message from Ann to be delivered to ' + destination)
        send.pretty_print()
        deliverable = send.serialize().encode()
        self.sockets['A'].sendall(deliverable)
