from router import Router
from agent import Agent

routing_table = {
        'A':   {'111': 0, 'B': 4,  'C': 3, 'E': 7},
        'B':   {'A': 4,   'C': 6,  'L': 5},
        'C':   {'A': 3,   'B': 6,  'D': 11},
        'D':   {'C': 11,  'G': 10, 'F': 6, 'L': 9},
        'E':   {'001': 0, 'A': 7,  'G': 5},
        'F':   {'100': 0, 'D': 6,  'L': 5},
        'G':   {'D': 10,  'E': 5},
        'H':   {'100': 0},
        'L':   {'B': 5,   'D': 9,  'F': 5},
        '111': {'A': 0},
        '001': {'E': 0},
        '100': {'F': 0,   'H': 0}
    }

def initialize_routers():
    routers = []
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'L']

    for r in labels:
        new_router = Router(name=r, args=(r, routing_table))
        routers.append(new_router)
        new_router.start()

    return routers

def initialize_agents():
    agents = []
    names = {'Ann':  '111',
             'Chan': '001',
             'Jan':  '100'}

    for agent_name, id in names.iteritems():
        new_agent = Agent(name=agent_name, args=(agent_name, id, routing_table))
        agents.append(new_agent)
        new_agent.start()

    return agents

routers = initialize_routers()
agents = initialize_agents()