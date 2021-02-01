import time
import datetime
import reader
import os

def priority (dist, age):
    return (dist * 2) + age + 1

def intToBool (n):
    return n == 1

def comparation (bydist, bycant, byage):
    return (intToBool (bydist) and intToBool (bycant)) or intToBool (byage)

class VersionCleaner:
    def __init__ (self, versions, settings):
        self.versions = versions
        self.toSave = []
        self.settings = settings

        self.savebycant = [0 for i in range (len (self.versions))]
        self.savebydist = [0 for i in range (len (self.versions))]
        self.savebyage  = [0 for i in range (len (self.versions))]

        self.prioritysave = [0 for i in range (len (self.versions))]

        self.save = [False for i in range (len (self.versions))]

    def addToSave (self, toAdd):
        for i in toAdd:
            if not self.toSave.count (i) == 1:
                self.toSave.append (i)

    def bycant (self):#Aplies to toSave list
        self.upperLimit = int (self.settings.get ("backupmaximumcant"))
        self.lowerLimit = int (self.settings.get ("backupminimumcant"))
        self.versioncant = len (self.toSave)

        self.prioritysave = [priority (self.savebydist [i], self.savebyage [i]) for i in range (len (self.versions))]
        self.addedAmount = 0
        for n in range (4, 0, -1):#Possible prioroties (1-4)
            if n <= 2 and self.addedAmount > self.lowerLimit: #Stop if priority is tolow and minimum cant is surpassed
                break
            if not self.addedAmount + self.prioritysave.count (n) >= self.upperLimit:#True if all the current version fit in
                for i in range (len (self.prioritysave) - 1, -1, -1):
                    if self.prioritysave [i] == n:
                        self.savebycant [i] = 1
                        self.addedAmount += 1
            else:
                for i in range (len (self.prioritysave) - 1, -1, -1):
                    if self.prioritysave [i] == n:
                        self.savebycant [i] = 1
                        self.addedAmount += 1
                        if self.addedAmount >= self.upperLimit:
                            break
                break

    def bydist (self):
        self.farEnough = []
        self.dists = []
        for i in range (0, len (self.versions) - 1):
            self.dists.append (abs ((datetime.timedelta (seconds = self.versions [i]) - datetime.timedelta (seconds = self.versions [i + 1])).total_seconds ()))
        self.separation = float (self.settings.get ("backupdistance")) * 60
        for i in range (0, len (self.dists)):
            if not self.dists [i] <= self.separation:
                self.savebydist [i] = 1
        self.savebydist [-1] = 1

    def byage (self):#Add young enough versions
        self.maxold = (datetime.timedelta (seconds = time.time ()) - datetime.timedelta (days = int (self.settings.get ("backupminimumage")))).total_seconds ()
        for i in range (0, len (self.versions)):
            if self.versions [i] >= self.maxold:
                self.savebyage [i] = 1
    
    def proccess (self):
        for i in range (len (self.versions)):
            self.save [i] = comparation (self.savebydist [i], self.savebycant [i], self.savebyage [i])


if __name__ == "__main__":
    c = VersionCleaner ([float (i) for i in os.listdir (r"E:\Copia de seguridad\Informatica")], reader.Config (r"D:\Informatica\Python\Copia de seguridad\backup\cleanerconfig.txt"))
    c.byage ()
    c.bydist ()
    c.bycant ()
    c.proccess ()
    print (c.save)