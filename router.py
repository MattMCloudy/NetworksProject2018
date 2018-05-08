import json
import sys
from packet import Packet
from client_server import ClientServer

class Router(ClientServer):
    def __init__(self, name, args):
        super(Router, self).__init__(name=name, args=args)
        self.destinations = {111: 'Ann', 1: 'Chan', 100: 'Jan'}

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
        dest = self.dijkstra(self.name, self.destinations[send.dest_port])
        self.sockets[dest[1]].sendall(deliverable)

    def dijkstra(self, start, end):
        # We always need to visit the start
        nodes_to_visit = {start}
        visited_nodes = set()
        # Distance from start to start is 0
        distance_from_start = {start: 0}
        tentative_parents = {}

        while nodes_to_visit:
            # The next node should be the one with the smallest weight
            current = min(
                [(distance_from_start[node], node) for node in nodes_to_visit]
            )[1]

            # The end was reached
            if current == end:
                break

            nodes_to_visit.discard(current)
            visited_nodes.add(current)

            edges = self.routing_table[current]
            unvisited_neighbours = set(edges).difference(visited_nodes)
            for neighbour in unvisited_neighbours:
                neighbour_distance = distance_from_start[current] + \
                                     edges[neighbour]
                if neighbour_distance < distance_from_start.get(neighbour,
                                                                float('inf')):
                    distance_from_start[neighbour] = neighbour_distance
                    tentative_parents[neighbour] = current
                    nodes_to_visit.add(neighbour)

        return self.deconstruct_path(tentative_parents, end)

    def deconstruct_path(self, tentative_parents, end):
        if end not in tentative_parents:
            return None
        cursor = end
        path = []
        while cursor:
            path.append(cursor)
            cursor = tentative_parents.get(cursor)
        return list(reversed(path))