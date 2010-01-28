import yaml
import bones
import barebones

def save(root, file):
    skeleton = barebones.Root(root)
    yaml.dump(skeleton, file)

def load(file):
    root = yaml.load(file)
    return root.to_root()
    
