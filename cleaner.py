import os
import time
import datetime

def getVersions (path):
    versions = []
    for i in os.listdir (path):
        if os.path.isdir (os.path.join (path, i)):
            try:
                versions.append (i)
            except:
                pass
    return versions

def timedeltatodays (delta):
    try:
        days = delta.days
    except:
        days = 0
    
    try:
        seconds = delta.seconds / 86400
    except:
        seconds = 0
    
    return days + seconds

def floattotime (time):
    return datetime.datetime.utcfromtimestamp (float (time))

class Versions:
    def __init__ (self, path, settings = None):
        self.versions = []
        self.temp = getVersions (path)
        for i in range (0, len (self.temp)):
            self.versions.append ({"float" : self.temp [i], "status" : True, "id" : i})
        if settings != None:
            self.settings = settings

    def settings (self, settings):
        self.settings = settings

    def getVersions (self, state = None):
        if state == None:
            return self.versions
        self.result = []
        for i in self.versions:
            if i["status"] == state:
                self.result.append (i)
        return self.result

    def byDistance (self):
        #Discriminate false
        self.useful = self.getVersions (True)
        for i in range (0, len (self.useful) - 1):
            self.separation = timedeltatodays(floattotime (self.useful [i]["float"]) - floattotime (self.useful [i + 1]["float"]))
            if self.separation <= self.settings ["backupdistance"]:
                self.versions [self.useful[i]["id"]]["status"] = False
        return self

if __name__ == "__main__":
    versions = Versions (r"E:\Copia de seguridad\Music", settings = {"backupdistance" : 2}).byDistance ().versions
    print (len (versions))
    for i in versions:
        print (i["status"], time.ctime (float (i["float"])))