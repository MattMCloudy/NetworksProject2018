import logging
from router import Router
from agent import Agent
from base import Base
from jan import Jan

def initialize_routers():
    routers = []
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'L']

    for r in labels:
        new_router = Router(name=r, args=(r, routes, routing_table))
        routers.append(new_router)
        new_router.start()

    return routers

def initialize_agents():
    agents = []
    names = ['Ann', 'Chan']
    for name in names:
        new_agent = Agent(name=name, args=(name, routes, routing_table))
        agents.append(new_agent)
        new_agent.start()

    jan = Jan(name='Jan', args=('Jan', routes, routing_table))
    agents.append(jan)
    jan.start()

    return agents

def initialize_base():
    base = Base(name='H', args=('H', routes, routing_table))
    base.start()
    return base

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')
routes = {'Ann': 111, 'Chan': 1, 'Jan': 100,
          'A': 8000, 'B':8001, 'C': 8002,
          'D': 8003, 'E': 8004, 'F': 8005,
          'G': 8006, 'H': 100, 'L': 8007}
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
routers = initialize_routers()
agents = initialize_agents()
base = initialize_base()