from math import pi

import matrix

def reload_bones_imports():
    reload(matrix)
    
class Joint:
    origin = matrix.Vector(0, 0)
    # Joints hold position and transformation relative to the root
    # This is considered ABSOLUTE
    def __init__(self):
        self.bones = []
        self.transform = matrix.Identity()
        self.position = matrix.Vector(0, 0)        

    def add_bone(self, bone):
        self.bones.append(bone)

    def __repr__(self):
        return "Joint:\n\tPos: " + str(self.position) + \
            "\n\tTransform:\n" + str(self.transform) + \
            "\n----------------------------"

    def calc_position(self):
        # You probably want to call calc_transform first!
        self.position = self.origin * self.transform

    def calc_skeleton(self):
        self.calc_position()
        for bone in self.bones:
            bone.calc_transform()
            bone.end.transform = bone.transform * self.transform
            bone.end.calc_skeleton()

class Bone:
    # Bones hold transformation information from start to end
    # This is considered RELATIVE
    def __init__(self, joint_from):
        joint_from.add_bone(self)
        self.start = joint_from
        self.end = Joint()
        self.rotation = 0
        self.length = 1
        self.transform = matrix.Identity()
        
    def __repr__(self):
        return "Bone:\nlength: %f\nrotation: %f\n"%(self.length, 
                                                    self.rotation) + \
                                                    str(self.transform)

    def calc_transform(self):
        self.transform = \
                       matrix.Translation(matrix.Vector(self.length, 0)) * \
                       matrix.Rotation(self.rotation)

def print_skeleton(root):
    print root
    for bone in root.bones:
        print bone
        print_skeleton(bone.end)

def test():
    root = Joint()
    b1 = Bone(root)
    b1.length = 50
    b1.rotation = pi / 2
    
    b2 = Bone(b1.end)
    b2.length = 100
    b2.rotation = 0

    print_skeleton(root)
    root.calc_skeleton()
    print "---"
    print_skeleton(root)

    
        
