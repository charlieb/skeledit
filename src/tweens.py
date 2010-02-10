import barebones
from copy import deepcopy
from time import time

class Keyframe:
    def __init__(self, root, time):
        self.root = root
        self.time = time

class Animation:
    min_keyframe_delta = 0.1
    def __init__(self):
        self.keyframes = []
        self.tweens = []
        self.playing = False
        self.start_time = 0.0

    def total_time(self):
        if self.keyframes != []:
            return self.keyframes[-1].time
        else:
            return 0.0

    def make_tweens(self):
        keys = self.keyframes
        self.tweens = []
        for i in range(len(self.keyframes) - 1):
            self.tweens.append(Tween(keys[i].root, keys[i+1].root,
                                     keys[i+1].time - keys[i].time))
            
    def get_state(self):
        total_time = self.start_time
        for tween in self.tweens:
            if total_time + tween.total_time > time():
                return tween.get_state_at(time() - total_time)
            total_time += tween.total_time
        self.playing = False

    def play_from(self, keyframe):
        self.make_tweens()
        self.playing = True
        self.start_time = time() - keyframe.time
        
class Tween():
    def __init__(self, start, end, time):
        '''start and end are barebones.Root objects'''
        self.start = start
        self.end = end
        self.diff = None
        self.total_time = time
        self.calc_diff()

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

        self.diff = deepcopy(self.start)
        calc_diff_r(self.start, self.end, self.diff)
                

    def get_state_at(self, time):
        def get_state_at_r(joint, start, diff):
            for i in range(0, len(joint.bones_out)):
                joint.bones_out[i].length = start.bones_out[i].length + \
                                            diff.bones_out[i].length * \
                                            (time / self.total_time)
                joint.bones_out[i].rotation = start.bones_out[i].rotation + \
                                              diff.bones_out[i].rotation * \
                                              (time / self.total_time)
                get_state_at_r(joint.bones_out[i].end,
                               start.bones_out[i].end,
                               diff.bones_out[i].end,)

        current = deepcopy(self.start)
        get_state_at_r(current, self.start, self.diff)
        return current
       
