import json
from dijsktra import Graph
from packet import Packet
from client_server import ClientServer

class Router(ClientServer):
    def __init(self, name, args):
        super(Router, self).__init__(name, args)
        self.labels = ['A','B','C','D','E','F','G','L']
        self.g_dict = {'Ann': 0, 'Chan': 4, 'Jan': 5}
        self.inverse_agent_routes = {111: 'Ann', 1: 'Chan', 100: 'Jan'}
        self.g = Graph(8).graph

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

        deliverable = send.serialize().encode()
        self.sockets[self.g.dijkstra(self.g_dict[self.inverse_agent_routes[send.src_port]], self.labels)].sendall(deliverable)
