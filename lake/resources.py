"""实际资源占用账与显式归还协议。"""
class Ledger:
    def __init__(self,memory,disk):self.memory=memory;self.disk=disk;self.used={};self.pending=set();self.events=[]
    def grant(self,operator,amount,disk=0):
        if min(amount,disk)<0:raise ValueError('资源不能为负')
        if sum(v[0] for v in self.used.values())+amount>self.memory or sum(v[1] for v in self.used.values())+disk>self.disk:raise ValueError('总资源不足')
        old=self.used.get(operator,(0,0));self.used[operator]=(old[0]+amount,old[1]+disk);self.events.append(['grant',operator,amount,disk])
    def request_revoke(self,operator):
        if operator not in self.used:raise ValueError('算子未分配')
        self.pending.add(operator);self.events.append(['revoke_requested',operator])
    def release(self,operator,amount,disk=0):
        old=self.used.get(operator,(0,0))
        if min(amount,disk)<0 or amount>old[0] or disk>old[1]:raise ValueError('归还超过占用')
        self.used[operator]=(old[0]-amount,old[1]-disk);self.events.append(['release',operator,amount,disk])

from .operators import Operator

def inspect(data,storage,root):
    ledger=Ledger(data['memory'],data['disk'])
    for op in data['operators']:ledger.grant(op['id'],op['min_resident'])
    return {'capacity':[data['memory'],data['disk']],'existing_reservations':ledger.used,'events':ledger.events}
