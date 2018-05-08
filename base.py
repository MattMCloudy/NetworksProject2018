import json
from packet import Packet
from client_server import ClientServer

class Base(ClientServer):
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

        send = Packet(src_port=self.routes['H'], dest_port=self.routes['Jan'])
        send.data = 'Mission Success'
        deliverable = send.serialize().encode()
        self.sockets['Jan'].sendall(deliverable)