import json
import sys
from packet import Packet
from client_server import ClientServer

class Router(ClientServer):
    def __init__(self, name, args):
        super(Router, self).__init__(name=name, args=args)
        self.labels = ['A','B','C','D','E','F','G','L']

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
        print(self.labels)

        print(self.dijkstra(self.labels.index(self.name), self.labels))
        self.sockets[self.labels[dest]].sendall(deliverable)

    def buildPath(self, parent, i, arr):
        if parent[i] == -1:
            return

        self.printPath(parent, parent[i], arr)
        arr += [i]
        print(arr)

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initilaize minimum distance for next node
        min = sys.maxsize

        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(8):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # Funtion that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src, label):

        dist = [sys.maxsize] * 8
        dist[src] = 0
        sptSet = [False] * 8
        parent = [0, 0, 0, 0, 0, 0, 0, 0]
        parent[src] = -1

        for cout in range(8):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shotest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(8):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        result = []
        self.buildPath(parent, src, result)
        return result