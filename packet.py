import json
from random import randint

class Packet():
    def __init__(self, src_port=None, dest_port=None, actor=None,
                 data=None, auth_code=None, seq_num=randint(1000, 9999), ack_num=None,
                 DRP=False, TER=False, URG=False, ACK=False, RST=False,
                 SYN=False, FIN=False):
        self.src_port = src_port
        self.dest_port = dest_port
        self.actor = actor
        self.data = data
        self.auth_code = auth_code
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.DRP = DRP
        self.TER = TER
        self.URG = URG
        self.ACK = ACK
        self.RST = RST
        self.SYN = SYN
        self.FIN = FIN

    def deserialize(self, data):
        self.src_port = data['src_port']
        self.dest_port = data['dest_port']
        self.actor = data['actor']
        self.data = data['data']
        self.auth_code = data['auth_code']
        self.seq_num = data['seq_num']
        self.ack_num = data['ack_num']
        self.DRP = data['DRP']
        self.TER = data['TER']
        self.URG = data['URG']
        self.ACK = data['ACK']
        self.RST = data['RST']
        self.SYN = data['SYN']
        self.FIN = data['FIN']

    def serialize(self):
        return json.dumps(self.__dict__)

    def acknowledgement(self, recv_packet):
        self.deserialize(recv_packet)
        self.ACK = True
        self.src_port = recv_packet['dest_port']
        self.dest_port = recv_packet['src_port']
        self.ack_num = recv_packet['seq_num']+1;
        if recv_packet['ACK'] == True:
            self.seq_num = recv_packet['ack_num']

    def pretty_print(self):
        for k, v in self.__dict__.items():
            print('Detailed Information: Packet Key ' + k + ' Has Value ' + str(v))