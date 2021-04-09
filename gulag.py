import os
import shutil
import gestor
import datetime
import time

class Gulag:
    def __init__ (self, path):
        self.versions = [gestor.getVersions (path)]

    def getOld (self):
        self.tooOld = []
        print ((datetime.timedelta (seconds = datetime.datetime.now ()) - datetime.timedelta (weeks = 1)).seconds)
        #for i in self.versions:



if __name__ == "__main__":
    print (time.time ())
    print (Gulag (r"E:\Copia de seguridad\- gulag\Informatica").getOld ())