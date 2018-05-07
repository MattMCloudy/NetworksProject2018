class Packet():
    def __init__(self, src_port=None, dest_port=None, actor=None,
                 data=None, auth_code=None, seq_num=None, ack_num=None,
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