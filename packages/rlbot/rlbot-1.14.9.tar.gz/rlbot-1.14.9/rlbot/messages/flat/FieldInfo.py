# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class FieldInfo(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFieldInfo(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FieldInfo()
        x.Init(buf, n + offset)
        return x

    # FieldInfo
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FieldInfo
    def BoostPads(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .BoostPad import BoostPad
            obj = BoostPad()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FieldInfo
    def BoostPadsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # FieldInfo
    def Goals(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .GoalInfo import GoalInfo
            obj = GoalInfo()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # FieldInfo
    def GoalsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def FieldInfoStart(builder): builder.StartObject(2)
def FieldInfoAddBoostPads(builder, boostPads): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(boostPads), 0)
def FieldInfoStartBoostPadsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def FieldInfoAddGoals(builder, goals): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(goals), 0)
def FieldInfoStartGoalsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def FieldInfoEnd(builder): return builder.EndObject()
