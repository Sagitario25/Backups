import os

def readFile (path):
    #Reads this programs config files and turns them into dicts
    readed = {}
    labels = []
    with open (path) as f:
        for i in f.readlines ():
            label, info = split (i)
            #Discard line
            if label == "end":#End line
                continue
            if i[0] == '#':#Line to ignore
                continue
            #Append to the list
            readed [label] = info[:-1].split ("#")[0]
            labels.append (label)
    return readed, labels

def split (config):
    #Divides a command line into label and info
    results = config.split ('>')
    return results [0], results [1]

class Config:
    def __init__ (self, path):
        self.contents, self.labels = readFile (path)
        for i in self.labels:
            self.times = self.labels.count (i)
            if self.times > 1:
                raise Exception (f'The "{i}" configuration in "{path}" is repeated {self.times} times. There must be only one.')
    
    def get (self, label):
        if self.labels.count (label) == 0:
            raise Exception ("That label doesn't exist")
        return self.contents [label]