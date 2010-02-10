import yaml
import bones
import barebones

def save_bones(root, file):
    skeleton = barebones.Root(root)
    yaml.dump(skeleton, file)

def load_bones(file):
    root = yaml.load(file)
    return root.to_root()
    
def save_keyframes(keyframes, file):
    yaml.dump(keyframes, file)
    
def load_keyframes(file):
    return yaml.load(file)
    
