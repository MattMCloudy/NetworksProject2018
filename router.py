import json
from packet import Packet
from client_server import ClientServer

class Router(ClientServer):
    def process_messages(self, connection, address):
        while True:
            data_json = connection.recv(1024)
            if not data_json: break
            data = json.loads(data_json.decode())
            self.log.debug('Message received from: ' + data['actor'])
            self.message_received(data)
        connection.close()

    def message_received(self, message):
        self.log.debug('Message data: '+message['data'])

        send = Packet()
        send.deserialize(message)
        send.src_port = self.routes[self.name]
        #TODO this is where we need to figure out the next port to send the packet

        send.dest_port = self.routes['DESTINATION NAME']

        deliverable = send.serialize().encode()
        self.sockets['DESTINATION NAME'].sendall(deliverable)
