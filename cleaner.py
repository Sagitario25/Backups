import time
import datetime
import reader

class VersionCleaner:
    def __init__ (self, versions, settings):
        self.versions = versions
        self.toSave = []
        self.settings = settings

    def addToSave (self, toAdd):
        for i in toAdd:
            if not self.toSave.count (i) == 1:
                self.toSave.append (i)

    def bycant (self):#Aplies to toSave list
        self.upperLimit = int (self.settings.get ("backupmaximumcant"))
        self.lowerLimit = int (self.settings.get ("backupminimumcant"))
        self.versioncant = len (self.toSave)
        if self.versioncant < self.lowerLimit:#Not enough versions
            for i in reversed (self.versions):
                self.addToSave (i)
                if self.versioncant == self.lowerLimit: break                
        elif self.versioncant > self.upperLimit and self.upperLimit != 0:#Too much versions
            self.toSave = self.toSave [self.versioncant - self.upperLimit:]
        elif self.versioncant >= self.lowerLimit and self.versioncant <= self.upperLimit:#Acceptable amount
            pass

    def bydist (self):
        self.farEnough = []
        self.dists = []
        for i in range (0, len (self.versions) - 1):
            self.dists.append ((datetime.timedelta (seconds = self.versions [i]) - datetime.timedelta (seconds = self.versions [i + 1])).total_seconds ())
        self.separation = float (self.settings.get ("backupdistance")) * 60
        for i in range (0, len (self.dists)):
            if self.dists [i] <= self.separation:
                self.addToSave ([self.versions [i]])

    def byage (self):#Add young enough versions
        self.maxold = (datetime.timedelta (seconds = time.time ()) - datetime.timedelta (days = int (self.settings.get ("backupminimumage")))).total_seconds ()
        for i in range (0, len (self.versions)):
            if self.versions [i] >= self.maxold:
                self.addToSave (self.versions [i:])
                break
        del self.maxold