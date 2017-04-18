# A license server clone

import socket
import threading
import time
import lic

# create a socket to listen for new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let socket be immidately reused
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind socket to port
s.bind(("", 50007))
# set socket to non blocking; this is weird on BSDs(osx)
# s.setblocking(False)
# listen!
s.listen(1)

lock = threading.Lock()
clients = []
usersOnline = []

#TODO: globals?
# the key is the productkey

class run_server(threading.Thread):
    def __init__ (self, conn):
        self.conn = conn
        self.socket = socket
        threading.Thread.__init__(self)


    def run(self):
        print threading.currentThread().getName()
        # lock and update the clients list
        lock.acquire()
        clients.append(self)
        lock.release()
        l = lic.LicServ()
        host = str(self.conn.getpeername())
        self.conn.send("Ready for data: ")
        self.data = self.conn.recv(1024).decode("latin1")
        self.textin = str(self.data).strip()
        # rpk is Requested Product Key
        rpk = self.textin
        if l.checkLicenseAvail(host, rpk):
            l.checkOutLic(host, rpk)
            self.conn.send("***************************************\n")
            self.conn.send("You got a lic " + host + rpk + "\n")
            self.conn.send("***************************************\n")
        else:
            self.conn.send("There is no license available for %s\n" %rpk )
        print l.totalLicenses
        print l.checkedOut

        #while 1:
            # take only latin strings, cuz italy
            #time.sleep(10)
        while 1:
            deadline = time.time() + 20.0
            self.conn.send("Do you still need a lic for %s\n" %rpk)
            self.conn.send("deadline is %s\n" %deadline)
            while not self.data:
                if time.time() >= deadline:
                    print "timed out"
                    l.returnLic(host, rpk)
                    break
            self.data = self.conn.recv(1024).decode("latin1")
            #self.conn.settimeout(deadline - time.time())
            self.textin = str(self.data).strip()
            print "received ", self.textin, "from client"
            #time.sleep(0.5)
            #self.conn.settimeout(None)
            #if not self.data: break

        lock.acquire()
        clients.remove(self)
        lock.release()
        self.conn.close()

threads = []
while 1:
    conn, addr = s.accept()
    print "connected", addr
    world = run_server(conn)
    world.start()
    threads.append(world)
    time.sleep(0.1)

s.close()
