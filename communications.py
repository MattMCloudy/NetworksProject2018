import logging.config
import time
import subprocess
from dijsktra import Graph
from router import Router
from base import Base
from jan import Jan
from ann import Ann
from chan import Chan

def initialize_routers():
    routers = []
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'L']
    i = 0

    for r in labels:
        new_router = Router(name=r, args=(r, routes, routing_table, graph))
        new_router.daemon = True
        new_router.start()
        routers.append(new_router)
        g = Graph(8)
        g.graph = graph
        g.dijkstra(i, r)
        i += 1

        time.sleep(1)

    return routers

def initialize_agents():
    agents = []

    ann = Ann(name='Ann', args=('Ann', routes, routing_table, graph))
    ann.daemon = True
    ann.start()
    agents.append(ann)
    time.sleep(1)

    chan = Chan(name='Chan', args=('Chan', routes, routing_table, graph))
    chan.daemon = True
    chan.start()
    agents.append(chan)
    time.sleep(1)

    jan = Jan(name='Jan', args=('Jan', routes, routing_table, graph))
    jan.daemon = True
    jan.start()
    agents.append(jan)

    return agents

def initialize_base():
    base = Base(name='H', args=('H', routes, routing_table, graph))
    base.daemon = True
    base.start()
    return base

def clean_routes():
    for name, route in routes.items():
        subprocess.Popen('lsof -t -i tcp:'+str(route)+'| xargs kill -9')

logging.config.fileConfig('logging.conf')
logging.debug('Logging Initiated')
routes = {'Ann': 111, 'Chan': 1, 'Jan': 100,
          'A': 8000, 'B':8001, 'C': 8002,
          'D': 8003, 'E': 8004, 'F': 8005,
          'G': 8006, 'H': 8007, 'L': 8008}
#clean_routes()
routing_table = {
        'A':   {'Ann': 0, 'B': 4,  'C': 3, 'E': 7},
        'B':   {'A': 4,   'C': 6,  'L': 5},
        'C':   {'A': 3,   'B': 6,  'D': 11},
        'D':   {'C': 11,  'G': 10, 'F': 6, 'L': 9},
        'E':   {'Chan': 0, 'A': 7,  'G': 5},
        'F':   {'Jan': 0, 'D': 6,  'L': 5},
        'G':   {'D': 10,  'E': 5},
        'H':   {'Jan': 0},
        'L':   {'B': 5,   'D': 9,  'F': 5},
        'Ann': {'A': 0},
        'Chan': {'E': 0},
        'Jan': {'F': 0,   'H': 0}
    }

graph = [[0,4, 3, 0,7,0, 0,0],
                  [4,0, 6, 0,0,0, 0,5],
                  [3,6, 0,11,0,0, 0,0],
                  [0,0,11, 0,0,6,10,9],
                  [7,0, 0, 0,0,0, 5,0],
                  [0,0, 0, 6,0,0, 0,5],
                  [0,0, 0,10,5,0, 0,0],
                  [0,5, 0, 9,0,5, 0,0]]

routers = initialize_routers()
agents = initialize_agents()
base = initialize_base()

while 1:
    time.sleep(10)
    print('AHH AHH AHH AHH STAYIN ALIVE STAYING ALIVE')
