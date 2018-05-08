import logging
import json
from client_server import ClientServer

class Chan(ClientServer):
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

        if message['TER'] == True:
            self.log.debug('Communication with Ann Terminated...')
            

