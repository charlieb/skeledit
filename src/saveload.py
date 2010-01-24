import yaml
import bones

class Joint:
    def __init__(self, joint):
        self.bones_out = [Bone(b) for b in joint.bones_out]

    def to_joint(self, bone_in):
        # bone_in is a bones.Bone
        joint = bones.Joint(bone_in)
        for b in self.bones_out:
            b.to_bone(joint)
        return joint
        
        
class Root(Joint):
    def __init__(self, joint):
        Joint.__init__(self, joint)

    def to_root(self):
        root = bones.Root()
        for b in self.bones_out:
            b.to_bone(root)
        return root

class Bone:
    def __init__(self, bone):
        self.end = Joint(bone.end)
        self.rotation = bone.rotation
        self.length = bone.length
        self.image = Image(bone.image) if bone.image else None

    def to_bone(self, start_joint):
        # start_joint is a bones.Joint
        bone = bones.Bone(start_joint)
        bone.rotation = self.rotation
        bone.length = self.length

        bone.end = self.end.to_joint(bone)
        bone.image = self.image.to_image(bone) if self.image else None
        return bone

class Image():
    def __init__(self, image):
        self.filename = image.filename
        self.rotation = image.rotation

    def __repr__(self):
        return "Image: %s\n\t%f"%(self.filename, self.rotation)

    def to_image(self, bone):
        # bone is a bones.Bone
        image = bones.Image(self.filename, bone)
        image.rotation = self.rotation
        return image

def save(root, file):
    skeleton = Root(root)
    yaml.dump(skeleton, file)

def load(file):
    root = yaml.load(file)
    return root.to_root()
    
