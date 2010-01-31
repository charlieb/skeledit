import bones

class Joint:
    def __init__(self, joint):
        self.bones_out = [Bone(b) for b in joint.bones_out]

    def set_joint(self, joint):
        for i in range(len(self.bones_out)):
            self.bones_out[i].set_bone(joint.bones_out[i])

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

    def _set_bone_values(self, bone):
        bone.rotation = self.rotation
        bone.length = self.length
        bone.image = self.image.to_image(bone) if self.image else None
        
    def set_bone(self, bone):
        self._set_bone_values(bone)
        self.end.set_joint(bone.end)

    def to_bone(self, start_joint):
        # start_joint is a bones.Joint
        bone = bones.Bone(start_joint)
        self._set_bone_values(bone)
        bone.end = self.end.to_joint(bone)
        return bone

class Image():
    def __init__(self, image):
        self.filename = image.filename
        self.rotation = image.rotation
        self.mirror_x = image.mirror_x
        self.mirror_y = image.mirror_y

    def __repr__(self):
        return "Image: %s\n\t%f"%(self.filename, self.rotation)

    def set_image(self, image):
        image.rotation = self.rotation
        image.mirror_x = self.mirror_x
        image.mirror_y = self.mirror_y

    def to_image(self, bone):
        # bone is a bones.Bone
        image = bones.Image(self.filename, bone)
        self.set_image(image)
        return image
