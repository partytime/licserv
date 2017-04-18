# the license functionality outside the serving?

import threading

lock = threading.Lock()


class LicServ(object):
    def __init__(self):
        #TODO: these will reset with every threaded instantiation
        self.totalLicenses = {"soft1":10,"soft2":1,"soft3":2}

        self.checkedOut = {"soft1":[],"soft2":[],"soft3":[]}
        #self.checkedOut = {"soft1":["10.82.4.5","10.82.4.7"]}
        pass

    def checkLicenseAvail(self, host, productKey):
        # Returns Bool
        if productKey not in self.totalLicenses:
            return False
        # We already have a license checked out
        elif host in self.checkedOut[productKey]:
            return True
        # There are available licenses
        elif len(self.checkedOut[productKey]) < self.totalLicenses[productKey]:
            return True
        # Nope
        return False

    def checkOutLic(self, host, productKey):
        lock.acquire()
        # Add the host to the keys value(list)
        self.checkedOut[productKey].append(host)
        # Decrement the total available at position productKey
        self.totalLicenses[productKey] -= 1
        lock.release()
        return

    def returnLic(self, host, productKey):
        lock.acquire()
        self.checkedOut[productKey].remove(host)
        self.totalLicenses[productKey] += 1
        lock.release()
        return

    def getAvailNumLic(self, productKey):
        # returns an int which is the val for the key productKey
        return len(self.totalLicenses[productKey])

    def getCheckedOutHosts(self, productKey):
        # returns a list object
        return self.checkedOut[productKey]


