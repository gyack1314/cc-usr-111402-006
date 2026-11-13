"""算子安全点与溢写确认的本地接口。"""
from .storage import canonical
class Operator:
    def __init__(self,identity,storage):self.identity=identity;self.storage=storage;self.buffers=[];self.spilled=[]
    def append(self,row):self.buffers.append(row)
    def resident(self):return sum(len(canonical(r)) for r in self.buffers)
    def spill_at_safe_point(self):
        size=self.resident();digest=self.storage.write(self.buffers);self.spilled.append(digest);self.buffers=[]
        return {'operator':self.identity,'released':size,'object':digest}
