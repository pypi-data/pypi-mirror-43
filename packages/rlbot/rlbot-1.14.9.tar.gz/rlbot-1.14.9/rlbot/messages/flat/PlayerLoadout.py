# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

# /// The car type, color, and other aspects of the player's appearance.
# /// See https://github.com/RLBot/RLBot/wiki/Bot-Customization
class PlayerLoadout(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsPlayerLoadout(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = PlayerLoadout()
        x.Init(buf, n + offset)
        return x

    # PlayerLoadout
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # PlayerLoadout
    def TeamColorId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def CustomColorId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def CarId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def DecalId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def WheelsId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def BoostId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def AntennaId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def HatId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def PaintFinishId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def CustomFinishId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def EngineAudioId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def TrailsId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(26))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def GoalExplosionId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # PlayerLoadout
    def LoadoutPaint(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(30))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .LoadoutPaint import LoadoutPaint
            obj = LoadoutPaint()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def PlayerLoadoutStart(builder): builder.StartObject(14)
def PlayerLoadoutAddTeamColorId(builder, teamColorId): builder.PrependInt32Slot(0, teamColorId, 0)
def PlayerLoadoutAddCustomColorId(builder, customColorId): builder.PrependInt32Slot(1, customColorId, 0)
def PlayerLoadoutAddCarId(builder, carId): builder.PrependInt32Slot(2, carId, 0)
def PlayerLoadoutAddDecalId(builder, decalId): builder.PrependInt32Slot(3, decalId, 0)
def PlayerLoadoutAddWheelsId(builder, wheelsId): builder.PrependInt32Slot(4, wheelsId, 0)
def PlayerLoadoutAddBoostId(builder, boostId): builder.PrependInt32Slot(5, boostId, 0)
def PlayerLoadoutAddAntennaId(builder, antennaId): builder.PrependInt32Slot(6, antennaId, 0)
def PlayerLoadoutAddHatId(builder, hatId): builder.PrependInt32Slot(7, hatId, 0)
def PlayerLoadoutAddPaintFinishId(builder, paintFinishId): builder.PrependInt32Slot(8, paintFinishId, 0)
def PlayerLoadoutAddCustomFinishId(builder, customFinishId): builder.PrependInt32Slot(9, customFinishId, 0)
def PlayerLoadoutAddEngineAudioId(builder, engineAudioId): builder.PrependInt32Slot(10, engineAudioId, 0)
def PlayerLoadoutAddTrailsId(builder, trailsId): builder.PrependInt32Slot(11, trailsId, 0)
def PlayerLoadoutAddGoalExplosionId(builder, goalExplosionId): builder.PrependInt32Slot(12, goalExplosionId, 0)
def PlayerLoadoutAddLoadoutPaint(builder, loadoutPaint): builder.PrependUOffsetTRelativeSlot(13, flatbuffers.number_types.UOffsetTFlags.py_type(loadoutPaint), 0)
def PlayerLoadoutEnd(builder): return builder.EndObject()
