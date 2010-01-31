import barebones
from copy import deepcopy

class Keyframe:
    def __init__(self, root, time):
        self.root = root
        self.time = time

class Animation:
    def __init__(self):
        self.keyframes = []
        self.tweens = []

    def make_tweens(self):
        keys = self.keyframes
        self.tweens = []
        for i in range(len(self.keyframes) - 1):
            tweens.append(Tween(keys[i].root, keys[i+1].root,
                                keys[i+1].time - keys[i].time))

    def add_keyframe(self, keyframe):
        self.keyframes.append(keyframe)
        
    def get_state_at(self, time):
        total_time = 0.0
        for tween in self.tweens:
            if total_time + tween.time > time:
                return tween.calc_current(time - total_time)
            
class Tween():
    def __init__(self, start, end, time):
        '''start and end are barebones.Root objects'''
        self.start = start
        self.end = end
        self.diff = None
        calc_diff()

        self.total_time = 10
        self.running = False

    def calc_diff(self):
        def calc_diff_r(start, end, diff):
            for i in range(len(start.bones_out)):
                diff.bones_out[i].length = end.bones_out[i].length - \
                                           start.bones_out[i].length
                                  
                diff.bones_out[i].rotation = end.bones_out[i].rotation - \
                                             start.bones_out[i].rotation
                calc_diff_r(start.bones_out[i].end,
                            end.bones_out[i].end,
                            diff.bones_out[i].end)

        self.diff = deepcopy(start)
        calc_diff_r(self.start, self.end, self.diff)
                

    def get_state_at(self, time): 
        def get_state_at_r(joint, start, diff):
            for i in range(0, len(joint.bones_out)):
                joint.bones_out[i].length = start.bones_out[i].length + \
                                            diff.bones_out[i] * \
                                            (time / self.time)
                joint.bones_out[i].rotation = start.bones_out[i].rotation + \
                                              diff.bones_out[i].rotation * \
                                              (time / self.time)
                get_state_at_r(joint.bones_out[i].end)

        current = deepcopy(self.start)
        get_state_at_r(current, self.start, self.diff)
        return current
       
