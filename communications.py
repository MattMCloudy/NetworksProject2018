import logging.config
import time
import subprocess
from router import Router
from agent import Agent
from base import Base
from jan import Jan

def initialize_routers():
    routers = []
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'L']

    for r in labels:
        new_router = Router(name=r, args=(r, routes, routing_table))
        new_router.daemon = True
        new_router.start()
        routers.append(new_router)
        time.sleep(1)

    return routers

def initialize_agents():
    agents = []
    names = ['Ann', 'Chan']
    for name in names:
        new_agent = Agent(name=name, args=(name, routes, routing_table))
        new_agent.daemon = True
        new_agent.start()
        agents.append(new_agent)
        time.sleep(1)

    jan = Jan(name='Jan', args=('Jan', routes, routing_table))
    jan.start()
    agents.append(jan)

    return agents

def initialize_base():
    base = Base(name='H', args=('H', routes, routing_table))
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

routers = initialize_routers()
agents = initialize_agents()
base = initialize_base()

