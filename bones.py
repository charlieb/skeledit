from matrix import Identity, Rotation, Translation, Scale, Vector
from math import pi

class Joint:
    # Joints hold position and transformation relative to the root
    # This is considered ABSOLUTE
    def __init__(self):
        self.bones = []
        self.transform = Identity()
        self.position = Vector(0, 0)        

    def add_bone(self, bone):
        self.bones.append(bone)

    def __repr__(self):
        return "Joint:\n" + str(self.transform)

    def calc_skeleton(self):
        for bone in self.bones:
            bone.calc_transform()
            bone.calc_end_position()
            bone.joint_to.transform = self.transform * bone.transform
            bone.joint_to.calc_skeleton()

class Root(Joint):
    def __init__(self):
        Joint.__init__(self)
        self.origin = Vector(0, 0)

    def __repr__(self):
        return "Root:\n" + str(self.position)        

class Bone:
    # Bones hold transformation information from start to end
    # This is considered RELATIVE
    def __init__(self, joint_from):
        joint_from.add_bone(self)
        self.start = joint_from
        self.end = Joint()
        self.rotation = 0
        self.length = 1
        self.transform = Identity()
        
    def __repr__(self):
        return "Bone:\nlength: %f\nrotation: %f\n"%(self.length, 
                                                    self.rotation) + \
                                                    str(self.transform)

    def calc_transform(self):
        self.transform = Rotation(self.rotation) * \
            Translation(Vector(0, self.length))
        print "calc_transform"
        print self.transform

    def calc_end_position(self):
        # You probably want to call calc_transform first!
        self.end.position = self.start.position * self.transform

def print_skeleton(root):
    print root
    for bone in root.bones:
        print bone
        print_skeleton(bone.joint_to)



def test():
    root = Root()
    b1 = Bone(root)
    b1.length = 5
    b2 = Bone(b1.joint_to)
    root.calc_skeleton()

    print "---"
    print_skeleton(root)

    
        
